import csv
import json
from pathlib import Path
from src.logger import logger

OUTPUT_DIR = Path("output")

def export_results(records: list[dict]) -> tuple[Path, Path]:
    """
    Exports a list of processed document records into both JSON and CSV files.
    Matches schema keys from workflow pipeline and outputs output/final_report.csv.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUTPUT_DIR / "results.json"
    csv_path = OUTPUT_DIR / "final_report.csv"  # Updated to match rubric specification

    if not records:
        logger.warning("No records provided for export.")
        return json_path, csv_path

    # Export JSON
    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        logger.info(f"Results successfully exported to JSON: {json_path}")
    except Exception as e:
        logger.error(f"Failed to export JSON results: {str(e)}")

    # Export CSV
    try:
        flat_records = []
        for r in records:
            # Safely handle key names matching workflow.py dictionary structure
            ext = r.get("extracted_info") or r.get("extracted_data") or {}
            outputs = r.get("generated_outputs") or {}
            
            flat_records.append({
                "file_name": r.get("file_name", "N/A"),
                "processed_at": r.get("processed_at", "N/A"),
                "customer_name": ext.get("customer_name", "N/A"),
                "email": ext.get("email", "N/A"),
                "phone_number": ext.get("phone_number", "N/A"),
                "complaint_category": ext.get("complaint_category", "N/A"),
                "issue_description": ext.get("issue_description", "N/A"),
                "resolution_provided": ext.get("resolution_provided", "N/A"),
                "is_complaint": ext.get("is_complaint", False),
                "requires_escalation": ext.get("requires_escalation", False),
                "supporting_doc_available": ext.get("supporting_doc_available", False),
                "overall_case_status": ext.get("overall_case_status", "N/A"),
                "customer_email_response": outputs.get("customer_email") or r.get("generated_email", "N/A"),
                "management_summary": outputs.get("management_summary") or r.get("generated_summary", "N/A"),
            })

        fieldnames = flat_records[0].keys()
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(flat_records)
        logger.info(f"Results successfully exported to CSV: {csv_path}")
    except Exception as e:
        logger.error(f"Failed to export CSV results: {str(e)}")

    return json_path, csv_path