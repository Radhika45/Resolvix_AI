import json
import re
from pydantic import ValidationError
from src.schema import ComplaintSchema
from src.logger import logger
from src.llm_handler import get_inference_engine

SYSTEM_PROMPT = """You are an expert enterprise document processing AI specializing in precision field extraction.
Your task is to read raw text from business complaint documents and extract structured metadata matching the exact requested JSON schema.

STRICT INSTRUCTIONS:
1. Extract values strictly based on the text provided. Do not hallucinate, guess, or invent details.
2. EMAIL EXTRACTION: Extract email addresses EXACTLY as written character-for-character (e.g., look for patterns like 'FROM: Name (email@domain.com)', 'Email: email@domain.com', or explicit headers).
3. PHONE EXTRACTION: Extract phone numbers character-for-character including country codes if provided.
4. If optional fields (email, phone_number, resolution_provided) are not present in the document, set them to null.
5. overall_case_status MUST strictly be one of: "Open", "Pending", "Resolved", or "Escalated".
6. Output ONLY valid JSON matching the exact schema. Do not include markdown blocks or extra text."""


def _fallback_regex_extract(raw_text: str) -> dict:
    """Regex fallback parser to extract email and phone numbers directly from text."""
    extracted = {}
    
    # Regex to find standard email addresses
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', raw_text)
    if email_match:
        extracted["email"] = email_match.group(0)

    # Regex to find standard phone numbers
    phone_match = re.search(r'\(?\+?\d{1,4}\)?[\s.-]?\(?\d{2,4}\)?[\s.-]?\d{3,4}[\s.-]?\d{3,4}', raw_text)
    if phone_match and len(re.sub(r'\D', '', phone_match.group(0))) >= 7:
        extracted["phone_number"] = phone_match.group(0)

    return extracted


def extract_structured_data(
    raw_text: str, 
    filename: str = "uploaded_file", 
    provider: str = "groq"
) -> tuple[ComplaintSchema | None, str]:
    """
    Extracts structured data from raw text using the configured LLM engine 
    and validates the response against ComplaintSchema.
    """
    if not raw_text or not raw_text.strip():
        logger.warning(f"Empty raw text passed for extraction: {filename}")
        return None, "FAILED_EMPTY_INPUT"

    schema_json = json.dumps(ComplaintSchema.model_json_schema(), indent=2)
    
    prompt = f"""Analyze the following complaint document and extract structured case details matching this JSON Schema:

JSON SCHEMA:
{schema_json}

CRITICAL EXTRACTION GUIDELINES:
- 'email': Search headers like 'FROM:', 'Email:', or text inside parentheses. Copy the exact email address.
- 'customer_name': Extract the full customer name filing the issue.
- 'phone_number': Extract contact phone numbers if present.
- 'overall_case_status': Choose strictly from ["Open", "Pending", "Resolved", "Escalated"].

DOCUMENT CONTENT:
---
{raw_text}
---

Return ONLY the populated JSON object."""

    try:
        logger.info(f"Sending '{filename}' to LLM Provider ({provider}) for structured extraction...")
        
        # Force temperature=0.0 for deterministic schema extraction
        llm = get_inference_engine(provider=provider, temperature=0.0)
        
        messages = [
            ("system", SYSTEM_PROMPT),
            ("user", prompt)
        ]
        
        response = llm.invoke(messages)
        raw_output = response.content if hasattr(response, 'content') else str(response)
        
        # Robust regex markdown strip for JSON strings
        cleaned_output = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_output.strip(), flags=re.MULTILINE).strip()

        # Parse output as dictionary for fallback checks
        extracted_dict = json.loads(cleaned_output)

        # Regex fallback for email and phone if LLM returned null
        regex_data = _fallback_regex_extract(raw_text)
        if not extracted_dict.get("email") and regex_data.get("email"):
            extracted_dict["email"] = regex_data["email"]
            logger.info(f"Regex fallback populated missing email: {regex_data['email']}")

        if not extracted_dict.get("phone_number") and regex_data.get("phone_number"):
            extracted_dict["phone_number"] = regex_data["phone_number"]
            logger.info(f"Regex fallback populated missing phone number: {regex_data['phone_number']}")

        # Validate extracted content against ComplaintSchema
        validated_data = ComplaintSchema.model_validate(extracted_dict)
        logger.info(f"Successfully extracted and validated data for: {filename}")
        return validated_data, "SUCCESS"

    except ValidationError as val_err:
        logger.error(f"Validation failure for '{filename}': {str(val_err)}")
        return None, "FAILED_VALIDATION"

    except Exception as e:
        logger.error(f"LLM execution failed for '{filename}' using provider '{provider}': {str(e)}")
        return None, "FAILED_LLM_INFERENCE"


class ContentExtractor:
    """Wrapper class to integrate extract_structured_data into workflow execution."""
    
    def __init__(self, provider: str = "groq"):
        self.provider = provider

    def extract_complaint_details(
        self, 
        raw_text: str, 
        filename: str = "uploaded_file", 
        provider: str = None
    ) -> ComplaintSchema:
        active_provider = provider or self.provider
        data, status = extract_structured_data(raw_text, filename, provider=active_provider)
        if status != "SUCCESS":
            raise ValueError(f"Extraction failed with status: {status}")
        return data