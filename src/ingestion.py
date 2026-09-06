from pathlib import Path
from typing import Dict, List, Tuple
import pypdf
import docx
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

from src.logger import logger

# Whitelist of supported file extensions (includes standard images)
SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".png", ".jpg", ".jpeg"}


def read_txt_file(file_path: Path) -> str:
    """Reads standard text files using UTF-8 encoding."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()


def ocr_pdf_file(file_path: Path) -> str:
    """Converts scanned PDF pages into images and runs Tesseract OCR."""
    try:
        images = convert_from_path(str(file_path))
        ocr_text = []
        for img in images:
            text = pytesseract.image_to_string(img)
            if text:
                ocr_text.append(text)
        return "\n".join(ocr_text).strip()
    except Exception as e:
        logger.error(f"Failed to perform OCR on PDF {file_path.name}: {str(e)}")
        return ""


def read_pdf_file(file_path: Path) -> str:
    """
    Extracts text content from PDF pages using pypdf.
    Falls back to OCR if digital text extraction yields negligible content.
    """
    reader = pypdf.PdfReader(file_path)
    text_content = []
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text_content.append(extracted)

    full_text = "\n".join(text_content).strip()

    # Fallback to OCR if page yields under 50 characters (scanned image PDF)
    if len(full_text) < 50:
        logger.info(f"PDF '{file_path.name}' appears to be a scanned image. Falling back to OCR...")
        return ocr_pdf_file(file_path)

    return full_text


def read_docx_file(file_path: Path) -> str:
    """Extracts paragraph text from Word documents using python-docx."""
    doc = docx.Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs).strip()


def read_image_file(file_path: Path) -> str:
    """Extracts text directly from image files (.png, .jpg, .jpeg) using Tesseract OCR."""
    try:
        img = Image.open(file_path)
        return pytesseract.image_to_string(img).strip()
    except Exception as e:
        logger.error(f"Failed to extract text from image {file_path.name}: {str(e)}")
        return ""


def extract_text_from_file(file_path: Path) -> Tuple[str, str]:
    """
    Determines format and extracts text content.
    Returns tuple: (extracted_text, status)
    """
    ext = file_path.suffix.lower()
    
    if ext not in SUPPORTED_EXTENSIONS:
        logger.warning(f"Skipping unsupported file extension: {file_path.name}")
        return "", "SKIPPED_UNSUPPORTED"

    try:
        if ext == ".txt":
            content = read_txt_file(file_path)
        elif ext == ".pdf":
            content = read_pdf_file(file_path)
        elif ext == ".docx":
            content = read_docx_file(file_path)
        elif ext in {".png", ".jpg", ".jpeg"}:
            content = read_image_file(file_path)
        else:
            return "", "SKIPPED_UNSUPPORTED"

        if not content:
            logger.warning(f"File is empty or contains no readable text: {file_path.name}")
            return "", "FAILED_EMPTY"

        return content, "SUCCESS"

    except Exception as e:
        logger.error(f"Error parsing file {file_path.name}: {str(e)}")
        return "", "FAILED_READ"


def scan_and_ingest_directory(data_dir: Path) -> List[Dict[str, str]]:
    """
    Scans data directory, processes all files, and returns batch metadata.
    """
    if not data_dir.exists() or not data_dir.is_dir():
        logger.error(f"Data directory not found: {data_dir}")
        return []

    ingested_records = []
    all_files = sorted(list(data_dir.iterdir()))

    logger.info(f"Scanning directory '{data_dir}' — Found {len(all_files)} total items.")

    for file_path in all_files:
        if file_path.is_file():
            text, status = extract_text_from_file(file_path)
            ingested_records.append({
                "file_name": file_path.name,
                "file_path": str(file_path),
                "extension": file_path.suffix.lower(),
                "status": status,
                "content": text
            })

    return ingested_records


class Ingestor:
    """Wrapper class to maintain compatibility across workflow calls."""
    @staticmethod
    def read_file(file_path: str) -> str:
        path_obj = Path(file_path)
        content, status = extract_text_from_file(path_obj)
        if status != "SUCCESS":
            raise ValueError(f"Failed to ingest file {path_obj.name} with status: {status}")
        return content