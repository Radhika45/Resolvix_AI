```markdown
<div align="center">

# 🚀 Resolvix AI
### Enterprise-Grade AI-Powered Customer Complaint & Case Processing System

An autonomous, multi-modal GenAI document intelligence workflow engineered to transform unstructured customer complaints into structured operational data, automated customer response dispatches, and executive summaries.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Groq Cloud](https://img.shields.io/badge/Inference-Groq%20Cloud-f50537?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com/)
[![Ollama](https://img.shields.io/badge/Local%20LLM-Ollama-000000?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.ai/)
[![Llama 3.2](https://img.shields.io/badge/Model-Meta%20Llama%203.2%20(3B)-0467DF?style=for-the-badge&logo=meta&logoColor=white)](https://ai.meta.com/llama/)
[![Pydantic v2](https://img.shields.io/badge/Validation-Pydantic%20v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![MongoDB Atlas](https://img.shields.io/badge/Database-MongoDB%20Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/cloud/atlas)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

[Live App Demo](https://resolvix-ai.streamlit.app) • [System Architecture](#-system-architecture) • [Installation Guide](#-installation-guide) • [Running Steps](#-running-the-application) • [Assessment Mapping](#-assessment-requirements-mapping)

</div>

---

## 📌 Project Overview

**Resolvix AI** addresses a fundamental operational bottleneck in customer service ecosystem: manual document triaging. High-volume customer support operations regularly ingest hundreds of unstructured complaint files in disparate formats (`.pdf`, `.docx`, `.txt`, scanned images). Processing these manually yields high resolution latency, inconsistent escalation tracking, missing customer metadata, and high operational costs.

### Why Traditional Approaches Fail
* **Brittle Regex Parsing:** Fails on dynamic, unformatted, or handwritten document variations.
* **Manual Data Entry:** Human support agents average 12–18 minutes per complaint to read, extract metrics, compose response emails, log database records, and draft manager summaries.
* **Lack of Concurrency Control:** Batch uploads frequently crash standard script pipelines due to thread starvation or downstream API rate limits.

### The AI-Powered Solution
Resolvix AI leverages a hybrid inference pipeline (**Groq LPU Acceleration** for production low latency with **Ollama Local LLM** offline fallbacks). Extracted outputs are guaranteed syntactically accurate using strict **Pydantic v2 schemas**. Asynchronous parallel execution (`asyncio`) reduces complete case processing—from document intake to SMTP response dispatch and MongoDB Atlas persistence—to **under 10 seconds per file**.

---

## 🌐 Live Demo

* 🚀 **Streamlit Cloud Deployment:** [https://resolvix-ai.streamlit.app](https://resolvix-ai.streamlit.app)
* 📹 **Video Walkthrough:** [Watch System Architecture & Demo](https://github.com/Radhika45/Resolvix_AI) *(Replace with video link)*
* 🐙 **GitHub Repository:** [https://github.com/Radhika45/Resolvix_AI](https://github.com/Radhika45/Resolvix_AI)

---

## 🎯 Problem Statement

Enterprise customer service organizations handle customer communications containing actionable metrics buried in chaotic narrative formats.


```

```
   UNSTRUCTURED INPUTS                                   MANUAL BOTTLENECK

```

┌───────────────────────────────┐                  ┌──────────────────────────────────┐
│  • Scanned Invoice Images     │                  │ • Slow manual document reading   │
│  • Multi-page PDF Reports     │ ───► BAD ──────► │ • Human error in metadata copy   │
│  • Word Complaint Letters     │                  │ • Untracked email notifications  │
│  • Unformatted Plain Text     │                  │ • Unstructured database records │
└───────────────────────────────┘                  └──────────────────────────────────┘
│
▼
RESOLVIX AI PIPELINE
┌──────────────────────────────────┐
│ • Automated Multi-Format Intake │
│ • OCR Engine for Image Extraction│
│ • Strict Pydantic LLM Parsing   │
│ • Parallel Asynchronous Dispatch │
│ • Instant Real-Time Storage      │
└──────────────────────────────────┘

```

---

## ✨ Key Features

| Category | Capability | Description |
| :--- | :--- | :--- |
| 📄 **Document Processing** | Multi-Format Extraction | Ingests `.pdf`, `.docx`, `.txt`, `.png`, and `.jpeg` complaint files seamless through native parsers and Tesseract OCR. |
| 🧠 **AI Intelligence** | Hybrid Engine | Uses Groq API Cloud Inference (`openai/gpt-oss-20b`) with an offline-capable Ollama fallback (`llama3.2`). |
| ✅ **Data Integrity** | Pydantic Schema Guardrails | Guarantees exact JSON key structure, data types, enumerations, and fallback defaults for zero runtime parsing errors. |
| 📧 **Customer Response** | Automated Email Drafting | Context-aware LLM prompts craft professional, empathetic response emails based on complaint severity. |
| 📋 **Executive Summaries** | Escalation Insights | Generates brief management summaries highlighting urgency levels, financial impacts, and required actions. |
| ⚡ **Async Throttling** | `asyncio.Semaphore` Engine | Limits parallel execution concurrency (`Semaphore(2)`) to prevent 429 Rate Limits during large batch file uploads. |
| 🗄 **Database Persistence** | MongoDB Atlas Cloud | Automatically syncs complete complaint structures, processed timestamps, and raw document payloads into central MongoDB databases. |
| 📨 **SMTP Auto-Dispatch** | Live Email Delivery | Validates generation outputs before executing real-time `smtplib` dispatch to the complainant's email address. |
| 📊 **Analytics Dashboard** | Streamlit Reporting | Interactive metric filtering, urgency distribution charts, and instant export of historical cases to CSV or JSON formats. |

---

## 🛠 Technology Stack


```

```
                           ┌────────────────────────────────┐
                           │     Streamlit Dashboard UI     │
                           └───────────────┬────────────────┘
                                           │
           ┌───────────────────────────────┼───────────────────────────────┐
           ▼                               ▼                               ▼

```

┌─────────────────────────┐     ┌─────────────────────────┐     ┌─────────────────────────┐
│   Ingestion Engine      │     │  AI Generation Core     │     │ Persistence & Delivery  │
├─────────────────────────┤     ├─────────────────────────┤     ├─────────────────────────┤
│ • PyPDF / Python-Docx   │     │ • Groq API (gpt-oss-20b)│     │ • MongoDB Atlas (PyMongo)│
│ • PyTesseract OCR       │     │ • Ollama (Llama 3.2 3B) │     │ • Python SMTP (Gmail)   │
│ • Pillow (PIL)          │     │ • Pydantic v2           │     │ • Exporter (CSV/JSON)   │
└─────────────────────────┘     └─────────────────────────┘     └─────────────────────────┘

```

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **User Interface** | `Streamlit v1.63+` | Provides an enterprise web interface for document uploads, schema views, and analytics. |
| **LLM Framework** | `LangChain Core / Groq / Ollama` | Orchestrates LLM prompt execution, multi-provider fallbacks, and retry wrappers. |
| **Data Validation** | `Pydantic v2` | Enforces rigid typing constraints on LLM output parsing to avoid structure degradation. |
| **Database** | `MongoDB Atlas` & `PyMongo` | NoSQL document storage storing unstructured and structured complaint payloads. |
| **Async Execution** | `asyncio` & `nest-asyncio` | Handles asynchronous file handling, parallelized generation calls, and non-blocking background tasks. |
| **OCR Processing** | `PyTesseract` & `Pillow` | Converts image-based complaints (`.png`, `.jpeg`) into clean plain text for downstream LLM processing. |
| **Document Parsers** | `PyPDF` & `python-docx` | Native text extraction from Microsoft Word documents and Adobe PDF reports. |
| **Communication** | `smtplib` & `email.mime` | Transmits auto-generated customer emails over TLS-encrypted SMTP server connections. |

---

## 🏛 System Architecture

```mermaid
graph TD
    A[User / Streamlit Interface] -->|Uploads PDF, DOCX, TXT, PNG| B[Ingestor Module]
    B -->|Check File Extension| C{Is Image?}
    C -- Yes --> D[PyTesseract OCR Engine]
    C -- No --> E[Native Document Reader]
    D --> F[Raw Complaint Text]
    E --> F
    F --> G[Workflow Orchestrator - asyncio]
    G -->|Throttled via Semaphore| H[Extractor Module]
    H -->|Groq / Ollama API| I[Pydantic v2 Schema Validation]
    I -->|Validated JSON Metadata| J[Parallel Generator Engine]
    J --> K[Customer Email Generator]
    J --> L[Executive Summary Generator]
    K --> M{Is Output Valid?}
    L --> N[Compile Final Document Payload]
    M -- Yes --> O[SMTP Service]
    O -->|Send Email| P[Customer Inbox]
    M -- No Error --> N
    N --> Q[MongoDB Atlas Sync]
    N --> R[Local File Output / CSV Export]

```

---

## 🔄 End-to-End Workflow

### Workflow 1: Complaint Extraction Pipeline

```
[Document Input] ──► [File Ingestor] ──► [OCR/Text Parsing] ──► [LangChain + Groq/Ollama] ──► [Pydantic Validation]

```

1. **Intake:** The file is streamed via Streamlit, copied into `data/` cache directory, and checked for binary composition.
2. **Parsing:** `.pdf` and `.docx` structures are parsed directly; bitmap image extensions trigger Tesseract OCR extraction.
3. **Structured Extraction:** The raw text payload is passed with a zero-shot system prompt to the configured LLM, enforcing JSON compliance matching the `ComplaintDetails` model.

### Workflow 2: Content Generation Pipeline

```
                              ┌──► [Generate Customer Email Response] ──┐
[Validated Data Schema] ──────┼─────────────────────────────────────────┼──► [Output Convergence]
                              └──► [Generate Management Summary] ───────┘

```

1. **Parallel Execution:** `asyncio.gather` spawns concurrent generator processes for email composition and management summary drafting.
2. **Context-Aware Prompting:** Extracted customer metrics, urgency ratings, and core issue descriptions are injected into dynamic system templates.
3. **Guardrail Check:** Output text is inspected for system errors (`ERROR:`) before authorizing downstream execution.

### Workflow 3: Persistence & Reporting Pipeline

```
                                 ┌──► [MongoDB Atlas Database Insert]
[Final Case Record Object] ──────┼──► [SMTP Transport Engine (Gmail)]
                                 └──► [CSV Report Synchronization]

```

1. **Email Delivery:** If a valid email address is extracted and no parsing errors occur, `send_customer_email` sends an automated reply over SMTP.
2. **Atlas Sync:** The unified record (raw input, extracted JSON schema, generated texts, execution timestamps) is persisted in MongoDB.
3. **CSV Export:** The full collection is exported to `output/results.csv` for analytics.

---

## 📂 Repository Structure

```text
Resolvix_AI/
├── .env.example               # Template for environment configuration secrets
├── .gitignore                 # Excludes venv, keys, and temporary output directories
├── README.md                  # System design, architecture, and deployment guide
├── requirements.txt           # Production environment dependencies
├── app.py                     # Streamlit web application & user interface entrypoint
├── data/                      # Input cache folder for uploaded complaint files
├── output/                    # Local storage repository for generated output artifacts
│   ├── case_summaries/        # Generated plain-text executive summaries
│   ├── customer_emails/       # Generated plain-text customer response letters
│   ├── structured_data/       # Generated validated JSON metadata files
│   └── results.csv            # Consolidated CSV export of processed database records
└── src/                       # Application code package
    ├── __init__.py            # Package initialization indicator
    ├── db.py                  # PyMongo client setup & MongoDB Atlas collection initialization
    ├── email_sender.py        # TLS-secured SMTP transport engine for automated emails
    ├── exporter.py            # Utility script converting MongoDB collections to CSV
    ├── extractor.py           # LLM extraction logic using Pydantic JSON schemas
    ├── generators.py          # Parallel LLM async generation tasks
    ├── ingestion.py           # Document ingestion router (PDF, Word, TXT, OCR)
    ├── llm_handler.py         # Provider initialization (Groq / Ollama) & retry policies
    ├── logger.py              # Centralized logging configuration
    ├── schema.py              # Pydantic v2 data structure definitions
    └── workflow.py            # Async process execution manager & semaphore controller

```

---

## 🗄 Database Schema

The system persists documents into MongoDB Atlas using the following schema structure:

```json
{
  "_id": "ObjectId('66db29f12a3b4c5d6e7f8a9b')",
  "file_name": "Complaint_Order_4091.pdf",
  "processed_at": "2026-09-06T15:30:00.000000+00:00",
  "raw_text": "Customer Sarah Connor reported unauthorized charges on Order #4091...",
  "extracted_info": {
    "customer_name": "Sarah Connor",
    "email": "sarah.c@sky.net",
    "phone": "+1-555-0199",
    "incident_date": "2026-09-02",
    "complaint_category": "Billing Error",
    "urgency_level": "High",
    "sentiment": "Frustrated",
    "summary": "Charged twice for subscription renewal ($299). Requests immediate refund."
  },
  "generated_outputs": {
    "customer_email": "Dear Sarah Connor,\n\nThank you for reaching out...",
    "management_summary": "HIGH URGENCY: Billing dispute received from Sarah Connor regarding Order #4091..."
  },
  "email_sent": true
}

```

---

## 📊 Extracted Data Schema

| Field Name | Type | Validation Rules | Description |
| --- | --- | --- | --- |
| `customer_name` | `String` | Default: `"Valued Customer"` | Full name extracted from signature or text body. |
| `email` | `String` | Regex Fallback Applied | Extracted customer email address for auto-reply. |
| `phone` | `String` | Default: `"N/A"` | Contact telephone number extracted from document text. |
| `incident_date` | `String` | Format: `YYYY-MM-DD` / `"N/A"` | Date when the reported incident or transaction occurred. |
| `complaint_category` | `Enum` | `Billing` | `Technical` | `Service` | `Delivery` | `Other` | Classified domain category of the complaint. |
| `urgency_level` | `Enum` | `Low` | `Medium` | `High` | `Critical` | Automated priority level based on sentiment and issue severity. |
| `sentiment` | `Enum` | `Positive` | `Neutral` | `Negative` | `Frustrated` | Emotional state detected from complaint language tone. |
| `summary` | `String` | Max 250 Characters | Concise single-sentence distillation of the customer's core complaint. |

---

## ⚙️ Installation Guide

### Prerequisites

* **Python:** Version `3.10` or higher
* **Tesseract OCR Engine:** Installed on system path *(Optional: Required only for image files)*
* *Windows:* Install via `UB-Mannheim/tesseract/wiki`
* *Linux:* `sudo apt-get install tesseract-ocr`
* *macOS:* `brew install tesseract`



### Step 1: Clone Repository

```bash
git clone [https://github.com/Radhika45/Resolvix_AI.git](https://github.com/Radhika45/Resolvix_AI.git)
cd Resolvix_AI

```

### Step 2: Initialize Virtual Environment

```powershell
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate

```

### Step 3: Install Required Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt

```

### Step 4: Install & Set Up Local Ollama Engine *(Optional for Offline Inference)*

1. Download and install Ollama from [ollama.ai](https://ollama.ai).
2. Pull the official Meta Llama 3.2 lightweight model:
```bash
ollama pull llama3.2

```



---

## 🔐 Environment Variables

Create a `.env` file in the project root directory matching the format below:

```ini
# --- LLM API PROVIDER CONFIGURATION ---
GROQ_API_KEY="gsk_your_groq_api_key_here"
GROQ_MODEL="openai/gpt-oss-20b"
OLLAMA_MODEL="llama3.2"

# --- DATABASE PERSISTENCE CONFIGURATION ---
MONGO_URI="mongodb+srv://<username>:<password>@cluster0.ku8ndcy.mongodb.net/complaint_management_db?retryWrites=true&w=majority"
DB_NAME="complaint_management_db"

# --- SMTP EMAIL DISPATCH CONFIGURATION ---
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT=587
SMTP_USERNAME="your_email@gmail.com"
SMTP_PASSWORD="your_gmail_app_password"

```

---

## 🚀 Running the Application

### 🖥️ Streamlit Web Dashboard Mode (Recommended)

Launch the primary web app interface:

```bash
streamlit run app.py

```

Open your browser and navigate to `http://localhost:8501`.

### 💻 Headless Batch Processing Mode (CLI Scripting)

Process files placed in `data/` via terminal commands without opening a browser:

```powershell
python -c "from src.workflow import ComplaintWorkflow; wf = ComplaintWorkflow(); print(wf.process_batch())"

```

---

## 💡 How to Use

1. **Access Web Interface:** Launch the Streamlit dashboard on localhost or navigate to the live deployment.
2. **Upload Documents:** Drag and drop single or multiple `.pdf`, `.docx`, `.txt`, `.png`, or `.jpeg` files into the upload box.
3. **Select Engine Provider:** Choose **Groq Cloud (Fast)** for high-performance cloud processing or **Ollama (Local)** for local execution.
4. **Execute Pipeline:** Click **Start AI Processing**.
5. **Inspect Live Results:**
* Review structured metadata fields parsed in real time.
* Read the auto-generated empathetic customer response email.
* View the management summary drafted for internal teams.


6. **Confirm Email Dispatch:** Verify if the real-time SMTP transport status indicates successful delivery.
7. **View Analytics & Export:** Switch to the **Analytics** tab to view historical case trends and download consolidated CSV or JSON files.

---

## 📝 Sample Input & Output

### Input Document (`Complaint_Order_4091.txt`)

```text
To Customer Support,

My name is Sarah Connor. My email address is sarah.c@sky.net.
On September 2nd, 2026, I noticed that my credit card was charged $299 twice for the renewal 
of my enterprise software subscription (Order #4091). I am extremely frustrated by this billing error. 
Please resolve this issue immediately and refund the duplicate charge of $299, or I will be forced to cancel my contract.

Regards,
Sarah Connor

```

### Extracted Schema Output (`output/structured_data/Complaint_Order_4091.json`)

```json
{
  "customer_name": "Sarah Connor",
  "email": "sarah.c@sky.net",
  "phone": "N/A",
  "incident_date": "2026-09-02",
  "complaint_category": "Billing Error",
  "urgency_level": "High",
  "sentiment": "Frustrated",
  "summary": "Customer charged twice ($299) for subscription renewal under Order #4091. Requests duplicate charge refund."
}

```

### Generated Response Email (`output/customer_emails/Complaint_Order_4091_email.txt`)

```text
Dear Sarah Connor,

Thank you for bringing this issue to our attention. We sincerely apologize for the frustration caused by the double charge on your credit card for Order #4091.

We have escalated your billing issue (Ref: Complaint_Order_4091.txt) directly to our finance team with High Priority. The duplicate charge of $299 is being reviewed for an immediate refund back to your original payment method.

You will receive an update within 24 hours. We value your business and appreciate your patience while we resolve this issue.

Best regards,
Customer Experience Support Team

```

### Management Executive Summary (`output/case_summaries/Complaint_Order_4091_summary.txt`)

```text
EXECUTIVE CASE SUMMARY
--------------------------------------------------
File Reference: Complaint_Order_4091.txt
Customer Name: Sarah Connor
Contact Email: sarah.c@sky.net
Category: Billing Error
Urgency Level: HIGH
Sentiment Tone: Frustrated

CORE INCIDENT DETAILS:
Customer was billed twice ($299 x 2) for Order #4091 on 2026-09-02. Customer has threatened contract cancellation if the duplicate $299 payment is not refunded promptly.

REQUIRED ACTION:
Finance department needs to issue an immediate $299 refund and confirm contract billing parameters.

```

---

## 🎯 Assessment Requirements Mapping

| Requirement | Technical Implementation | Status |
| --- | --- | --- |
| **Multi-Format Ingestion** | Implemented `Ingestor` supporting PDF, DOCX, TXT, and OCR for images. | ✅ Complete |
| **Structured LLM Extraction** | Implemented Pydantic models enforced with LangChain ChatGroq/Ollama APIs. | ✅ Complete |
| **Automated Response Generation** | Contextual system prompts generate tailored response emails. | ✅ Complete |
| **Executive Case Summaries** | Parallelized LLM prompts format executive management summaries. | ✅ Complete |
| **Async Workflow Design** | Built `asyncio` batch pipelines managed via `asyncio.Semaphore(2)` throttling. | ✅ Complete |
| **Database Persistence** | Cloud integration saving operational records directly to MongoDB Atlas collections. | ✅ Complete |
| **SMTP Auto-Dispatch** | Integrated `smtplib` engine with regex validations preventing corrupted dispatches. | ✅ Complete |
| **Production UI** | Built Streamlit application featuring live progress indicators, JSON viewers, and analytics. | ✅ Complete |

---

## 🛠 Engineering Challenges & Solutions

### 1. API Rate Limits (HTTP 429) During Parallel Processing

* **Challenge:** Processing multiple large complaint files simultaneously triggered HTTP 429 rate limit exceptions on Groq API endpoints.
* **Solution:** Introduced a global `asyncio.Semaphore(2)` in `src/workflow.py` to control concurrent LLM requests without blocking UI responsiveness.

### 2. Dispatches of Unformatted Error Texts via SMTP

* **Challenge:** When API calls timed out, exception strings were accidentally passed into the email generator, sending error text to customers.
* **Solution:** Added output validation in `workflow.py` checking for `ERROR:` prefixes, suppressing SMTP dispatch if generation fails.

### 3. Virtual Environment Path Corruption After Directory Rename

* **Challenge:** Renaming the root project directory broke absolute paths hardcoded inside Python virtual environment execution scripts.
* **Solution:** Re-initialized environment paths and automated dependency sync using clean `pip freeze` manifests.

---

## 🔮 Future Enhancements

* [ ] **RAG Architecture:** Vectorize company policies into ChromaDB to allow grounded policy lookups during email generation.
* [ ] **Agentic Multi-Step Graph:** Upgrade workflow to **LangGraph** to support dynamic human-in-the-loop approvals before sending emails for critical issues.
* [ ] **Containerization:** Package application dependencies into Docker containers for deployment to Kubernetes (EKS/GKE) clusters.
* [ ] **Enterprise Access Control:** Implement Role-Based Access Control (RBAC) separating support agents from management review teams.

---

## 🧠 Key Learnings & Takeaways

* **Structured Output Guardrails:** Using Pydantic schemas with LLMs eliminates output format unpredictability in enterprise production pipelines.
* **Asynchronous Concurrency Throttling:** Applying semaphores prevents API rate limiting during parallelized GenAI execution.
* **Hybrid Model Architecture:** Designing systems with cloud inference engines and local fallback options ensures high availability.

---

## 👩‍💻 Author

**Radhika**

*B.Tech - Computer Science & Engineering*

PCTE Institute of Engineering & Technology (Class of 2026)

* **GitHub:** [@Radhika45](https://github.com/Radhika45)
* **LinkedIn:** [Connect on LinkedIn](https://linkedin.com) *(Replace with profile URL)*
* **Live App Link:** [Resolvix AI Streamlit Dashboard](https://www.google.com/url?sa=E&source=gmail&q=https://resolvix-ai.streamlit.app)
* **Project Repository:** [Resolvix_AI Source Repository](https://www.google.com/url?sa=E&source=gmail&q=https://github.com/Radhika45/Resolvix_AI)

---

## 🙏 Acknowledgements

* [Streamlit Community Cloud](https://streamlit.io/cloud) for hosting public web applications.
* [Groq Cloud Platform](https://groq.com/) for LPU-accelerated inference APIs.
* [Ollama](https://ollama.ai) & [Meta AI](https://ai.meta.com/) for open-access Llama 3.2 model weights.
* [LangChain](https://www.langchain.com/) & [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) for orchestration and database tools.

---

Here is the complete, submission-ready **`README.md`** file customized for your project.

---

```markdown
# 🚀 Resolvix AI: AI Customer Complaint & Case Processing System

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://resolvix-ai.streamlit.app)
![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Framework](https://img.shields.io/badge/LLM Framework-LangChain-orange.svg)
![Model Engine](https://img.shields.io/badge/Inference-Groq Cloud%2F%20Ollama-green.svg)
![Database](https://img.shields.io/badge/Storage-MongoDB%20Atlas-brightgreen.svg)
![Deployment](https://img.shields.io/badge/Deployment-Streamlit%20Community%20Cloud-red.svg)

---

## 🌐 Live Demo
Access the live, fully production-ready application online:  
👉 **[https://resolvix-ai.streamlit.app](https://resolvix-ai.streamlit.app)**

---

## 🎯 Problem Statement
In modern enterprise customer service operations, resolving incoming customer complaints manually is slow, error-prone, and inefficient. Support agents spend countless hours manually inspecting unstructured documents (`.pdf`, `.docx`, `.txt`), extracting key metrics, writing tailored response emails, creating internal escalation summaries, and logging data.

**Resolvix AI** solves this problem by automating the end-to-end processing pipeline—from unstructured document ingestion to structured metadata extraction, real-time parallel generation of customer response emails and executive summaries, automated SMTP email dispatch, and database persistence in under 10 seconds per case.

---

## 💡 Project Overview
Resolvix AI is an enterprise-grade document processing and complaint management workflow powered by LangChain and Groq API Cloud Inference (with local Ollama offline fallback). It features:
1. **Parallel Execution:** Asynchronous processing (`asyncio`) allows extracting metadata, crafting customer emails, and writing management summaries simultaneously without blocking UI threads.
2. **Concurrency Throttling:** Built-in `asyncio.Semaphore` logic prevents rate limits (HTTP 429) during bulk multi-file uploads.
3. **Automated Customer Dispatch:** Real-time email delivery using standard SMTP (Gmail integration).
4. **Structured JSON Extraction:** Pydantic schema validation ensures reliable downstream analytical persistence into MongoDB Atlas and CSV exports.

---

## ✨ Features
* 📄 **Multi-Format Ingestion:** Native parsing support for `.pdf`, `.docx`, `.txt`, `.png`, and `.jpeg` complaint files.
* ⚡ **High-Speed Inference:** Groq Cloud LPU integration (`openai/gpt-oss-20b`) delivering instantaneous structured extractions.
* 🔀 **Hybrid LLM Provider:** Dynamic switching between cloud inference (Groq) and local execution (Ollama).
* 🛡️ **Hardened Robustness:** Extraction regex backstopping for contact info and programmatic error checks prior to sending automated SMTP emails.
* 📊 **Analytics Dashboard:** Historical case analysis, priority breakdowns, sentiment distribution, and bulk export directly from Streamlit UI.

---

## 🛠 Technology Stack

* **Frontend Dashboard:** Streamlit
* **LLM Orchestration:** LangChain, LangChain-Groq, LangChain-Ollama
* **Data Validation:** Pydantic v2
* **Storage & Persistence:** MongoDB Atlas (PyMongo), Local File Artifact Storage, CSV Exporters
* **Communication Protocol:** Python `smtplib` (Gmail App Password)
* **Concurrent Runtime:** `asyncio`, `nest-asyncio`

---

## 🏛 Architecture Diagram


```

[ Uploaded Files (.pdf/.docx/.txt) ]
│
▼
[ Streamlit UI Dashboard ]
│
▼
[ Ingestor Engine Module ]
│
▼
┌─────────────────────────────────────────────────────────┐
│            Workflow Engine (Concurrency Managed)        │
│                                                         │
│  [Extractor] -> Structured Extraction (Pydantic Schema)│
│                         │                               │
│                         ▼                               │
│        [Parallel Generator Engine (asyncio)]            │
│            ├── Customer Email Generator                 │
│            └── Executive Case Summary Generator         │
└─────────────────────────────────────────────────────────┘
│
┌───────┴────────────────────────┬────────────────────────┐
▼                                ▼                        ▼
[ SMTP Email Dispatch ]      [ MongoDB Atlas Sync ]    [ File Artifacts Export ]
(Real Customer Email)         (Centralized DB)          (JSON / CSV Output)

```

---

## 🔄 Workflow Diagram


```

[User Uploads Complaints] -> [Save to Data Storage] -> [Extract Metadata via LLM]
│
▼
[Update Dashboard UI] <─ [Save Artifacts] <─ [SMTP Dispatch] <─ [Generate Email & Summary in Parallel]

```

---

## 📂 Repository Structure

```text
Resolvix_AI/
├── .env                       # Local environment secrets (Git-ignored)
├── README.md                  # Detailed project documentation
├── requirements.txt           # Python dependency tree
├── app.py                     # Streamlit application main entry point
├── data/                      # Input raw documents cache directory
├── output/                    # Processed case output artifacts
│   ├── case_summaries/        # Generated executive summaries
│   ├── customer_emails/       # Formatted response emails
│   └── structured_data/       # Structured JSON exports
└── src/                       # Core system modular source code
    ├── __init__.py
    ├── db.py                  # MongoDB Atlas database client connection
    ├── email_sender.py        # Automated SMTP dispatch utility
    ├── exporter.py            # Local JSON and CSV export management
    ├── extractor.py           # Structured extraction via LangChain/Pydantic
    ├── generators.py          # Parallel LLM output generation functions
    ├── ingestion.py           # Multi-format document text reader
    ├── llm_handler.py         # Provider initialization & retry logic
    ├── logger.py             # System execution logger configuration
    ├── schema.py              # Pydantic data schemas for complaints
    └── workflow.py            # Orchestrating batch workflow and asyncio logic

```

---

## 🗄 Database Schema

The system stores complaints in the MongoDB Atlas `complaint_management_db` collection:

```json
{
  "_id": "ObjectId('65f12a34b56c7d8e9f012345')",
  "file_name": "Complaint_Order_4091.pdf",
  "processed_at": "2026-09-06T15:30:00.000000+00:00",
  "raw_text": "Full extracted document text content...",
  "extracted_info": {
    "customer_name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0199",
    "incident_date": "2026-09-01",
    "complaint_category": "Billing Error",
    "urgency_level": "High",
    "sentiment": "Negative",
    "summary": "Charged twice for subscription renewal."
  },
  "generated_outputs": {
    "customer_email": "Dear John Doe, ...",
    "management_summary": "High urgency billing dispute received from John Doe..."
  },
  "email_sent": true
}

```

---

## 📊 Data Schema Table

| Parameter | Data Type | Requirement | Description |
| --- | --- | --- | --- |
| `customer_name` | String | Required | Extracted name of the aggrieved customer. |
| `email` | String | Required | Extracted recipient email address for auto-reply. |
| `phone` | String | Optional | Extracted customer telephone contact. |
| `incident_date` | String | Optional | Date when the reported issue occurred. |
| `complaint_category` | Enum | Required | Categorization (e.g., Billing, Technical, Service). |
| `urgency_level` | Enum | Required | Assigned priority: Low, Medium, High, Critical. |
| `sentiment` | Enum | Required | Assessed tone: Positive, Neutral, Negative, Frustrated. |
| `summary` | String | Required | One-sentence distillation of the core complaint issue. |

---

## ⚙️ Installation Guide

### Prerequisites

* Python 3.10 or higher installed on your local machine.
* Git version control tool.

### Local Setup

1. **Clone the Repository:**
```bash
git clone [https://github.com/Radhika45/Resolvix_AI.git](https://github.com/Radhika45/Resolvix_AI.git)
cd Resolvix_AI

```


2. **Create and Activate a Virtual Environment:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

```


3. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


4. **Launch Application Locally:**
```bash
streamlit run app.py

```



---

## 🔑 Environment Variables

Create a local `.env` file or configure your cloud provider secrets with the following key-value pairs:

```toml
GROQ_API_KEY = "gsk_your_groq_api_key_here"
GROQ_MODEL = "openai/gpt-oss-20b"
OLLAMA_MODEL = "llama3.2"

MONGO_URI = "mongodb+srv://<user>:<password>@cluster.mongodb.net/complaint_management_db"
DB_NAME = "complaint_management_db"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your_email@gmail.com"
SMTP_PASSWORD = "your_gmail_app_password"

```

---

## 💻 Usage Guide

1. Navigate to the **Process Complaints** page on the Streamlit dashboard.
2. Drag and drop single or multiple customer complaint documents (`.pdf`, `.docx`, or `.txt`).
3. Click **Start AI Batch Processing**.
4. View real-time output tabs:
* **Extracted Schema Details:** Verified structured metadata.
* **Generated Customer Email:** Tailored response ready for/dispatched via email.
* **Management Executive Summary:** Brief high-level summary for escalation teams.


5. Inspect real-time status indicating if the email was automatically dispatched to the customer via SMTP.
6. Open the **Analytics & Exports** tab to view historical case statistics and download consolidated CSV reports.

---

## 🖼️ Screenshots

*(Add screenshots of your deployed Streamlit UI dashboard here)*

* **Main Dashboard Upload View**
* **Real-time Processing & Email Status**
* **Analytics and MongoDB Historical Query Screen**

---

## 📝 Sample Input/Output

### Sample Input (`Complaint_Sample.txt`)

> "My name is Sarah Connor (sarah.c@sky.net). On September 2nd, I was charged $299 twice for my enterprise software license renewal. I need an immediate refund for the extra charge or I will cancel my contract."

### Sample Output (`structured_data/Complaint_Sample.json`)

```json
{
  "customer_name": "Sarah Connor",
  "email": "sarah.c@sky.net",
  "phone": "N/A",
  "incident_date": "2026-09-02",
  "complaint_category": "Billing Error",
  "urgency_level": "High",
  "sentiment": "Frustrated",
  "summary": "Customer charged twice ($299) for enterprise license renewal and requests an immediate refund."
}

```

---

## 🎯 Assessment Requirement Mapping

| Assessment Requirement | Technical Implementation | Status |
| --- | --- | --- |
| **Document Ingestion** | Supports parsing text from PDF, Word documents, and text files. | ✅ Complete |
| **Structured LLM Extraction** | Pydantic Schema output enforced with LangChain ChatGroq. | ✅ Complete |
| **Parallel Execution** | `asyncio.gather` for dual output generation (Email & Summary). | ✅ Complete |
| **Email Auto-Dispatch** | Real-time `smtplib` dispatch with HTML formatting and error checking. | ✅ Complete |
| **Database Persistence** | MongoDB Atlas Cloud integration for full complaint history storage. | ✅ Complete |
| **Production Deployment** | Hosted live on Streamlit Community Cloud with encrypted secrets. | ✅ Complete |

---

## 🔮 Future Enhancements

* **OCR Support for Handwritten Scans:** Integrate Tesseract engine into standard ingestion workflow.
* **Multi-Language Translation:** Add automatic localization support to translate non-English complaints before processing.
* **Agentic Escalation Routes:** Integrate LangGraph agents to assign escalated tickets directly into standard ticketing APIs like Jira or Zendesk.

---

## 👩‍💻 Author Section

**Developed by:** Radhika

* **GitHub:** [@Radhika45](https://github.com/Radhika45)
* **Live App Link:** [Resolvix AI Streamlit Application](https://www.google.com/url?sa=E&source=gmail&q=https://resolvix-ai.streamlit.app)
* **Project Repository:** [Resolvix_AI Source Code](https://www.google.com/search?q=https://github.com/Radhika45/Resolvix_AI)

```

```