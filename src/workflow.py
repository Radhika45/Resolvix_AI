import os
import json
import asyncio
from datetime import datetime, timezone
from pathlib import Path

from src.ingestion import Ingestor
from src.extractor import ContentExtractor
from src.generators import TextGenerator, generate_outputs_in_parallel
from src.db import complaints_collection
from src.exporter import export_results
from src.email_sender import send_customer_email
from src.logger import logger

# Global semaphore to throttle concurrent LLM API calls and prevent 429 rate limit errors
MAX_CONCURRENT_LLM_CALLS = 2
llm_semaphore = asyncio.Semaphore(MAX_CONCURRENT_LLM_CALLS)


class ComplaintWorkflow:
    def __init__(self, data_dir: str = "data", output_dir: str = "output", provider: str = "groq"):
        self.provider = provider
        self.ingestor = Ingestor()
        self.extractor = ContentExtractor(provider=self.provider)
        self.generator = TextGenerator(provider=self.provider)
        
        # Base folder paths matching project directory tree
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        
        # Output subdirectories
        self.summaries_dir = self.output_dir / "case_summaries"
        self.emails_dir = self.output_dir / "customer_emails"
        self.structured_dir = self.output_dir / "structured_data"

        # Create directories if they do not exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.summaries_dir.mkdir(parents=True, exist_ok=True)
        self.emails_dir.mkdir(parents=True, exist_ok=True)
        self.structured_dir.mkdir(parents=True, exist_ok=True)

    async def process_file_async(self, file_path: str, save_to_data_folder: bool = True) -> dict:
        """
        Asynchronously processes a single complaint file:
        1. Ingests raw document text.
        2. Extracts structured LLM metadata with concurrency throttling.
        3. Generates customer email response and case summary in parallel with concurrency throttling.
        4. Dispatches real-time SMTP automated email notification to the customer if generation succeeded.
        5. Saves output artifacts to physical subfolders, MongoDB Atlas, and CSV report.
        """
        source_path = Path(file_path)
        file_name = source_path.name
        
        # 1. Save input document into actual data/ folder if needed
        target_data_path = self.data_dir / file_name
        if save_to_data_folder and source_path.resolve() != target_data_path.resolve():
            file_bytes = await asyncio.to_thread(source_path.read_bytes)
            await asyncio.to_thread(target_data_path.write_bytes, file_bytes)
            file_path_to_use = str(target_data_path)
        else:
            file_path_to_use = str(source_path)

        # 2. Ingest document text
        raw_text = await asyncio.to_thread(self.ingestor.read_file, file_path_to_use)

        # 3. Extract structured details via LLM (Throttled using semaphore)
        async with llm_semaphore:
            structured_data = await asyncio.to_thread(
                self.extractor.extract_complaint_details, 
                raw_text, 
                filename=file_name, 
                provider=self.provider
            )

        if hasattr(structured_data, "model_dump"):
            extracted_dict = structured_data.model_dump()
        elif hasattr(structured_data, "dict"):
            extracted_dict = structured_data.dict()
        else:
            extracted_dict = structured_data

        # 4. Generate AI Outputs in PARALLEL via asyncio (Throttled using semaphore)
        async with llm_semaphore:
            customer_email, management_summary = await generate_outputs_in_parallel(
                extracted_dict, filename=file_name, provider=self.provider
            )

        # 5. AUTOMATED SMTP EMAIL DELIVERY INTEGRATION (Only if email generation succeeded)
        recipient_email = extracted_dict.get("email")
        customer_name = extracted_dict.get("customer_name", "Valued Customer")
        email_subject = f"Update Regarding Your Support Request - Ref: {file_name}"
        
        email_sent_status = False
        if recipient_email and customer_email and not customer_email.startswith("ERROR:"):
            logger.info(f"Attempting SMTP auto-dispatch to {recipient_email} for {file_name}...")
            try:
                email_sent_status = await asyncio.to_thread(
                    send_customer_email,
                    recipient_email=recipient_email,
                    subject=email_subject,
                    body=customer_email
                )
            except Exception as e:
                logger.error(f"Failed to send email to {recipient_email}: {e}")
        elif customer_email and customer_email.startswith("ERROR:"):
            logger.warning(f"Skipping SMTP dispatch for {file_name} due to email generation error.")

        # 6. Save output artifacts to disk matching output folder structure
        base_stem = Path(file_name).stem
        
        def _write_outputs():
            # Save structured JSON
            with open(self.structured_dir / f"{base_stem}.json", "w", encoding="utf-8") as f:
                json.dump(extracted_dict, f, indent=4)
                
            # Save customer email text
            with open(self.emails_dir / f"{base_stem}_email.txt", "w", encoding="utf-8") as f:
                f.write(customer_email)
                
            # Save management summary text
            with open(self.summaries_dir / f"{base_stem}_summary.txt", "w", encoding="utf-8") as f:
                f.write(management_summary)

        await asyncio.to_thread(_write_outputs)

        # 7. MongoDB record construction
        complaint_record = {
            "file_name": file_name,
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "raw_text": raw_text,
            "extracted_info": extracted_dict,
            "generated_outputs": {
                "customer_email": customer_email,
                "management_summary": management_summary
            },
            "email_sent": email_sent_status
        }

        # Save to MongoDB Atlas & update final CSV export safely
        def _db_operations():
            try:
                if complaints_collection is not None:
                    complaints_collection.insert_one(complaint_record)
                    all_records = list(complaints_collection.find({}, {"_id": 0}))
                    export_results(all_records)
            except Exception as e:
                logger.error(f"Database sync/export failed for {file_name}: {e}")

        await asyncio.to_thread(_db_operations)

        # Strip ObjectId for downstream rendering compatibility
        complaint_record.pop("_id", None)
        return complaint_record

    def _run_sync(self, coro):
        """Helper execution loop to run async coroutines safely without crashing Streamlit or existing event loops."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import nest_asyncio
                nest_asyncio.apply()
                return loop.run_until_complete(coro)
            else:
                return loop.run_until_complete(coro)
        except RuntimeError:
            return asyncio.run(coro)

    def process_file(self, file_path: str, save_to_data_folder: bool = True) -> dict:
        """Synchronous wrapper for processing a single file."""
        return self._run_sync(self.process_file_async(file_path, save_to_data_folder))

    async def process_file_paths_async(self, file_paths: list[str]) -> list[dict]:
        """
        Asynchronously processes ONLY the explicitly passed uploaded file paths in parallel.
        Prevents re-processing previously processed files sitting in data/.
        """
        logger.info(f"Starting parallel processing for {len(file_paths)} newly uploaded file(s).")
        tasks = [self.process_file_async(fp, save_to_data_folder=False) for fp in file_paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        processed_records = []
        for fp, res in zip(file_paths, results):
            if isinstance(res, Exception):
                logger.error(f"Failed to process {fp}: {str(res)}")
            else:
                processed_records.append(res)

        logger.info(f"Targeted batch processing complete. Processed {len(processed_records)} file(s).")
        return processed_records

    async def process_batch_async(self) -> list[dict]:
        """
        Asynchronously processes all eligible .pdf, .docx, and .txt files in data/ in parallel.
        """
        logger.info(f"Starting parallel batch processing in directory: {self.data_dir}")
        supported_extensions = {".pdf", ".docx", ".txt", ".png", ".jpg", ".jpeg"}
        
        file_paths = [
            str(p) for p in self.data_dir.iterdir()
            if p.is_file() and p.suffix.lower() in supported_extensions
        ]

        if not file_paths:
            logger.warning("No eligible files found in data/ directory.")
            return []

        tasks = [self.process_file_async(fp, save_to_data_folder=False) for fp in file_paths]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        processed_records = []
        for fp, res in zip(file_paths, results):
            if isinstance(res, Exception):
                logger.error(f"Failed to batch process {fp}: {str(res)}")
            else:
                processed_records.append(res)

        # Save consolidated run result in output/results.json
        results_file = self.output_dir / "results.json"
        
        def _save_batch_results():
            with open(results_file, "w", encoding="utf-8") as f:
                json.dump(processed_records, f, indent=2)

        await asyncio.to_thread(_save_batch_results)

        logger.info(f"Parallel batch processing complete. Processed {len(processed_records)} files.")
        return processed_records

    def process_batch(self) -> list[dict]:
        """Synchronous wrapper for batch processing."""
        return self._run_sync(self.process_batch_async())