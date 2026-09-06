import os
import asyncio
import pandas as pd
from pathlib import Path
import streamlit as st

from src.auth import authenticate_user
from src.workflow import ComplaintWorkflow
from src.db import complaints_collection
from src.email_sender import send_customer_email

# Helper database function
def get_all_complaints():
    try:
        return list(complaints_collection.find({}, {"_id": 0}))
    except Exception as e:
        st.error(f"Failed to fetch records from MongoDB: {e}")
        return []

st.set_page_config(
    page_title="AI Complaint Intelligence System",
    page_icon="📋",
    layout="wide"
)

# --- SESSION STATE AUTHENTICATION ---
if "user" not in st.session_state:
    st.session_state.user = None

def login_form():
    st.title("🔑 Login — AI Complaint Management System")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign In")
        
        if submitted:
            user = authenticate_user(username, password)
            if user:
                st.session_state.user = user
                st.success(f"Welcome back, {user['name']}!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

if st.session_state.user is None:
    login_form()
    st.stop()

# --- MAIN APP INTERFACE ---
user = st.session_state.user

# Sidebar Configuration
st.sidebar.title(f"👤 {user['name']}")
st.sidebar.caption(f"Role: **{user['role']}**")

# Engine Switching Control
provider = st.sidebar.selectbox(
    "Select LLM Engine Provider",
    options=["groq", "ollama"],
    index=0,
    help="Groq handles ultra-fast cloud inference. Ollama runs locally on your machine."
)

workflow = ComplaintWorkflow(provider=provider)

st.sidebar.markdown("---")
if st.sidebar.button("Log Out"):
    st.session_state.user = None
    st.rerun()

st.title("📋 AI Complaint Management & Analytics Dashboard")

# Role-Based Navigation Tabs
if user['role'] == "Admin":
    tab1, tab2, tab3 = st.tabs(["📤 Live Processing", "📊 Analytics Dashboard", "📋 All Records"])
else:
    tab1, tab3 = st.tabs(["📤 Live Processing", "📋 All Records"])
    tab2 = None

# TAB 1: Live Multi-File Upload & Processing
with tab1:
    st.subheader("Process New Complaint Documents")
    
    uploaded_files = st.file_uploader(
        "Upload complaint files (.txt, .pdf, .docx, .png, .jpg, .jpeg)",
        type=["txt", "pdf", "docx", "png", "jpg", "jpeg"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("Process Selected Complaints", type="primary"):
            with st.spinner(f"Saving files and executing AI pipeline with provider [{provider.upper()}]..."):
                temp_dir = Path("data")
                temp_dir.mkdir(exist_ok=True)
                
                # 1. Save uploaded files to data/ folder and isolate file paths
                target_file_paths = []
                for uploaded_file in uploaded_files:
                    target_path = temp_dir / uploaded_file.name
                    with open(target_path, "wb") as f:
                        f.write(uploaded_file.getvalue())
                    target_file_paths.append(str(target_path))
                
                try:
                    # 2. Process uploaded files using workflow event loop helper
                    if hasattr(workflow, "process_file_paths_async"):
                        results = workflow._run_sync(workflow.process_file_paths_async(target_file_paths))
                    else:
                        results = workflow._run_sync(workflow.process_batch_async())
                    
                    st.success(f"Successfully processed {len(results)} document(s)!")
                    
                    # Display results for processed items
                    for item in results:
                        st.divider()
                        fn = item.get("file_name", item.get("filename", "Unknown"))
                        st.markdown(f"#### 📄 File: `{fn}`")
                        
                        outputs = item.get("generated_outputs", {})
                        extracted = item.get("extracted_info", {})
                        recipient_email = extracted.get("email", "Not Found")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("### 📧 Generated Customer Email Response")
                            st.caption(f"Recipient Email: **{recipient_email}**")
                            
                            email_text = st.text_area(
                                "Customer Email Content", 
                                outputs.get("customer_email", "N/A"), 
                                height=220, 
                                key=f"email_{fn}"
                            )
                            
                            # Email Delivery Status & Resend Functionality
                            is_sent = item.get("email_sent", False)
                            if is_sent:
                                st.success(f"✅ Email automatically dispatched to {recipient_email} via SMTP!")
                            else:
                                st.warning(f"⚠️ Email auto-dispatch pending or failed for {recipient_email}.")
                            
                            # Manual Resend Action
                            if st.button(f"📤 Resend Email via SMTP", key=f"resend_{fn}"):
                                if recipient_email and recipient_email != "Not Found":
                                    subject = f"Update Regarding Your Support Request - Ref: {fn}"
                                    success = send_customer_email(recipient_email, subject, email_text)
                                    if success:
                                        st.success(f"Email successfully delivered to {recipient_email}!")
                                    else:
                                        st.error("Failed to deliver email. Please verify SMTP configuration in .env.")
                                else:
                                    st.error("Cannot send email: No valid recipient email address was extracted.")

                        with col2:
                            st.markdown("### 📝 Management Summary")
                            st.text_area(
                                "Summary Content", 
                                outputs.get("management_summary", "N/A"), 
                                height=280, 
                                key=f"summary_{fn}"
                            )

                except Exception as e:
                    st.error(f"Error executing processing pipeline: {e}")

# TAB 2: Analytics Dashboard (Admin Only)
if tab2:
    with tab2:
        st.subheader("Analytics Overview")
        complaints = get_all_complaints()
        
        if complaints:
            df = pd.json_normalize(complaints)
            
            # Key Metrics
            total_cases = len(df)
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Complaints Processed", total_cases)
            
            if "extracted_info.overall_case_status" in df.columns:
                resolved_cnt = len(df[df["extracted_info.overall_case_status"] == "Resolved"])
                col2.metric("Resolved Cases", resolved_cnt)
            
            if "extracted_info.urgency_level" in df.columns:
                high_urgency = len(df[df["extracted_info.urgency_level"].isin(["High", "Critical"])])
                col3.metric("High/Critical Urgency", high_urgency)

            st.divider()
            
            # Breakdown Charts
            c1, c2 = st.columns(2)
            if "extracted_info.complaint_category" in df.columns:
                with c1:
                    st.markdown("**Complaints by Category**")
                    st.bar_chart(df["extracted_info.complaint_category"].value_counts())
            
            if "extracted_info.urgency_level" in df.columns:
                with c2:
                    st.markdown("**Complaints by Urgency**")
                    st.bar_chart(df["extracted_info.urgency_level"].value_counts())

        else:
            st.info("No complaint data available yet. Upload and process a file in Tab 1 first.")

# TAB 3: All Records
with tab3:
    st.subheader("Complaint Records Registry")
    records = get_all_complaints()
    if records:
        df_records = pd.json_normalize(records)
        st.dataframe(df_records, width="stretch")
    else:
        st.info("No records found in database.")