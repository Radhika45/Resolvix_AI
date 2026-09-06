from typing import Literal, Optional
from pydantic import BaseModel, Field


class ComplaintSchema(BaseModel):
    """
    Pydantic schema representing the extracted target fields
    from customer complaint documents.
    """
    customer_name: str = Field(
        default="Unknown",
        description="Full name of the customer filing the complaint or inquiry. Set to 'Unknown' if missing."
    )
    email: Optional[str] = Field(
        default=None, 
        description="Customer email address if available."
    )
    phone_number: Optional[str] = Field(
        default=None, 
        description="Customer contact phone number if available."
    )
    complaint_category: str = Field(
        default="General Inquiry", 
        description="Broad category of the issue (e.g., Billing Issue, Product Defect, Service Delay)."
    )
    issue_description: str = Field(
        default="No detailed description provided.", 
        description="Detailed summary of the core issue reported by the customer."
    )
    resolution_provided: Optional[str] = Field(
        default=None, 
        description="Actions or resolutions already communicated or taken by support."
    )
    is_complaint: bool = Field(
        default=True, 
        description="True if document reflects an actual grievance/complaint, False if general inquiry."
    )
    requires_escalation: bool = Field(
        default=False, 
        description="True if case requires manager/tier-2 escalation, False otherwise."
    )
    supporting_doc_available: bool = Field(
        default=False, 
        description="True if customer attached/mentioned supporting docs/photos/receipts."
    )
    overall_case_status: Literal["Open", "Pending", "Resolved", "Escalated"] = Field(
        default="Open", 
        description="Current workflow status of the case. Must strictly be one of: 'Open', 'Pending', 'Resolved', 'Escalated'."
    )