import asyncio
import re
from src.schema import ComplaintSchema
from src.logger import logger
from src.llm_handler import get_inference_engine

EMAIL_SYSTEM_PROMPT = """You are an elite customer service communications manager.
Your task is to draft a polite, concise, and highly professional customer response email based strictly on the provided case data.

STRICT RULES:
1. Do NOT invent details, dates, monetary amounts, or facts not present in the input.
2. Address the customer by name if available; otherwise use 'Valued Customer'.
3. Briefly summarize the issue acknowledged and state the current case status / resolution steps.
4. Maintain a reassuring, respectful corporate tone.
5. Do NOT include markdown code blocks around the email text. Return plain readable email text.
6. Do NOT leave generic bracket placeholders like [Company Name] or [Contact Information]. Sign off cleanly as 'Customer Support Team'."""

SUMMARY_SYSTEM_PROMPT = """You are a senior business operations analyst.
Your task is to write a structured executive summary brief based strictly on the provided case data.

STRICT RULES:
1. Follow the exact 5-section format requested.
2. Be concise, objective, and factual.
3. Do NOT invent facts or details outside the provided structured data.
4. Return clean, plain formatted text without markdown code blocks."""


def _ensure_schema(data) -> ComplaintSchema:
    """Helper function to parse dictionaries into ComplaintSchema instances."""
    if isinstance(data, ComplaintSchema):
        return data
    if isinstance(data, dict):
        return ComplaintSchema(**data)
    raise ValueError(f"Unsupported data type for generation: {type(data)}")


def _clean_markdown(text: str) -> str:
    """Strips outer markdown code block tags if present."""
    return re.sub(r"^```(?:txt|text|markdown)?\s*|\s*```$", "", text.strip(), flags=re.MULTILINE).strip()


async def generate_customer_email(
    data, 
    filename: str = "uploaded_file", 
    provider: str = "groq"
) -> str:
    """Generates a customer response email from ComplaintSchema data."""
    schema = _ensure_schema(data)
    
    prompt = f"""Draft a professional customer response email using the following case record:

Customer Name: {schema.customer_name}
Category: {schema.complaint_category}
Issue Description: {schema.issue_description}
Resolution Provided: {schema.resolution_provided or 'Under review by our support team'}
Case Status: {schema.overall_case_status}
Requires Escalation: {schema.requires_escalation}
"""
    try:
        logger.info(f"Generating customer response email for '{filename}' via {provider}...")
        
        llm = get_inference_engine(provider=provider, temperature=0.3)
        messages = [
            ("system", EMAIL_SYSTEM_PROMPT),
            ("user", prompt)
        ]
        
        # Native async invocation with thread-executor fallback
        if hasattr(llm, "ainvoke"):
            response = await llm.ainvoke(messages)
        else:
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(None, llm.invoke, messages)
        
        raw_text = response.content if hasattr(response, 'content') else str(response)
        email_text = _clean_markdown(raw_text)

        # Replace all signature and placeholder tags with actual values
        email_text = (
            email_text
            .replace("[Your Name]", "Radhika")
            .replace("[Your name]", "Radhika")
            .replace("[Company Name]", "Customer Experience Operations")
            .replace("[Company name]", "Customer Experience Operations")
            .replace("[Contact Information]", "support@enterprise.com")
            .replace("[Contact information]", "support@enterprise.com")
            .replace("[Phone Number]", "1-800-555-0199")
        )

        logger.info(f"Customer email generated successfully for: {filename}")
        return email_text

    except Exception as e:
        logger.error(f"Failed to generate customer email for '{filename}': {str(e)}")
        return "ERROR: Customer email generation failed."


async def generate_case_summary(
    data, 
    filename: str = "uploaded_file", 
    provider: str = "groq"
) -> str:
    """Generates a 5-section internal management brief from ComplaintSchema data."""
    schema = _ensure_schema(data)

    prompt = f"""Generate an internal executive case summary brief using the following record:

Customer Name: {schema.customer_name}
Email: {schema.email or 'N/A'}
Phone: {schema.phone_number or 'N/A'}
Category: {schema.complaint_category}
Issue Description: {schema.issue_description}
Resolution Action: {schema.resolution_provided or 'None recorded'}
Is Complaint: {schema.is_complaint}
Requires Escalation: {schema.requires_escalation}
Supporting Docs: {schema.supporting_doc_available}
Overall Case Status: {schema.overall_case_status}

Please structure the output into these EXACT 5 sections:
1. Case Overview
2. Key Issue
3. Action Taken
4. Current Status
5. Recommended Next Action
"""
    try:
        logger.info(f"Generating executive case summary for '{filename}' via {provider}...")
        
        llm = get_inference_engine(provider=provider, temperature=0.3)
        messages = [
            ("system", SUMMARY_SYSTEM_PROMPT),
            ("user", prompt)
        ]
        
        if hasattr(llm, "ainvoke"):
            response = await llm.ainvoke(messages)
        else:
            loop = asyncio.get_running_loop()
            response = await loop.run_in_executor(None, llm.invoke, messages)
        
        raw_text = response.content if hasattr(response, 'content') else str(response)
        summary_text = _clean_markdown(raw_text)
        
        logger.info(f"Executive summary generated successfully for: {filename}")
        return summary_text

    except Exception as e:
        logger.error(f"Failed to generate case summary for '{filename}': {str(e)}")
        return "ERROR: Case summary generation failed."


class TextGenerator:
    """Wrapper class to integrate generator functions into workflow execution."""
    
    def __init__(self, provider: str = "groq"):
        self.provider = provider

    def _run_async(self, coro):
        """Helper method to safely execute async functions in synchronous contexts."""
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

    def generate_customer_email(self, data, filename: str = "uploaded_file") -> str:
        return self._run_async(generate_customer_email(data, filename, provider=self.provider))

    def generate_management_summary(self, data, filename: str = "uploaded_file") -> str:
        return self._run_async(generate_case_summary(data, filename, provider=self.provider))


async def generate_outputs_in_parallel(
    data, 
    filename: str = "uploaded_file", 
    provider: str = "groq"
) -> tuple[str, str]:
    """Executes customer email generation and management summary generation concurrently."""
    logger.info(f"Starting parallel generation of email and summary for: {filename}")
    
    customer_email, management_summary = await asyncio.gather(
        generate_customer_email(data, filename, provider=provider),
        generate_case_summary(data, filename, provider=provider)
    )
    
    return customer_email, management_summary