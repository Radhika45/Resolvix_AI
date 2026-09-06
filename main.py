import sys
import argparse
from src.workflow import ComplaintWorkflow
from src.logger import logger


def main():
    parser = argparse.ArgumentParser(
        description="AI Document Processor - Enterprise Batch Processing & Structured Extraction Pipeline"
    )
    parser.add_argument(
        "--provider",
        type=str,
        default="groq",
        choices=["groq", "ollama"],
        help="LLM provider engine to use for extraction and generation (default: groq)",
    )
    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="Path to a single file to process. If omitted, processes all files in data/",
    )

    args = parser.parse_args()

    logger.info(f"Initializing AI Document Processor pipeline with provider: '{args.provider}'...")
    workflow = ComplaintWorkflow(provider=args.provider)

    if args.file:
        logger.info(f"Targeted single-file processing mode initialized for: {args.file}")
        try:
            result = workflow.process_file(args.file)
            print("\n" + "=" * 50)
            print("SINGLE FILE PROCESSING COMPLETE")
            print("=" * 50)
            print(f"File Name      : {result.get('file_name')}")
            print(f"Customer Name  : {result.get('extracted_info', {}).get('customer_name')}")
            print(f"Case Status    : {result.get('extracted_info', {}).get('overall_case_status')}")
            print(f"Email Sent     : {result.get('email_sent')}")
            print("=" * 50 + "\n")
        except Exception as e:
            logger.error(f"Single file processing failed: {str(e)}")
            sys.exit(1)
    else:
        logger.info("Batch processing mode initialized for all documents in data/...")
        try:
            results = workflow.process_batch()
            print("\n" + "=" * 50)
            print(f"BATCH PROCESSING COMPLETE - Processed {len(results)} file(s)")
            print("=" * 50)
            for res in results:
                print(f"• File: {res.get('file_name')} | Status: {res.get('extracted_info', {}).get('overall_case_status')} | Email Dispatched: {res.get('email_sent')}")
            print("=" * 50 + "\n")
        except Exception as e:
            logger.error(f"Batch processing failed: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    main()