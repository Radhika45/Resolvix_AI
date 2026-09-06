# 🚀 Resolvix AI

### AI-Powered Customer Complaint & Case Processing System

Resolvix AI is an intelligent document-processing platform that automates the handling of customer complaints and support cases. The system converts unstructured documents into structured business data, generates customer response emails, creates executive summaries, and stores processed records for analytics and reporting.

---

## 📌 Problem Statement

Customer support teams receive complaints in various formats such as PDFs, Word documents, text files, and scanned images. Manually reviewing these documents is time-consuming, error-prone, and difficult to scale.

Resolvix AI automates this workflow by:

* Extracting key complaint information
* Classifying complaint severity
* Generating customer response emails
* Creating management summaries
* Persisting records in MongoDB
* Providing analytics through a Streamlit dashboard

---

## ✨ Key Features

### 📄 Multi-Format Document Processing

Supports:

* PDF (`.pdf`)
* Word (`.docx`)
* Text (`.txt`)
* Images (`.png`, `.jpg`, `.jpeg`)

### 🤖 AI-Powered Information Extraction

Extracts structured complaint data including:

* Customer Name
* Email Address
* Phone Number
* Complaint Category
* Incident Date
* Urgency Level
* Sentiment
* Complaint Summary

### 🛡 Structured Output Validation

Uses **Pydantic v2** schemas to ensure consistent and reliable JSON outputs.

### 📧 Automated Response Generation

Creates professional customer response emails based on complaint details and severity.

### 📋 Executive Summary Generation

Generates concise management summaries highlighting:

* Key issue
* Customer impact
* Urgency level
* Recommended action

### ⚡ Asynchronous Processing

Utilizes `asyncio` and `Semaphore` controls to process multiple files efficiently while preventing API rate-limit issues.

### 🗄 Database Persistence

Stores:

* Raw document text
* Extracted structured data
* Generated outputs
* Processing metadata

in **MongoDB Atlas**.

### 📊 Analytics Dashboard

Interactive Streamlit dashboard for:

* Complaint monitoring
* Sentiment analysis
* Urgency distribution
* Data export

---

## 🏗 System Architecture

```text
                    ┌──────────────────┐
                    │   Streamlit UI   │
                    └─────────┬────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Document Ingestor│
                    └─────────┬────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
      OCR Processing                   Text Parsing
     (Images Only)                (PDF/DOCX/TXT Files)

              └───────────────┬───────────────┘
                              ▼
                  ┌──────────────────────┐
                  │ AI Extraction Engine │
                  │  Groq / Ollama LLM   │
                  └──────────┬───────────┘
                             ▼
                  ┌──────────────────────┐
                  │ Pydantic Validation  │
                  └──────────┬───────────┘
                             ▼
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
   Customer Email     Executive Summary    MongoDB Save
      Generator          Generator
```

---

## 🛠 Technology Stack

| Layer            | Technologies              |
| ---------------- | ------------------------- |
| Frontend         | Streamlit                 |
| LLM Providers    | Groq, Ollama              |
| Orchestration    | LangChain                 |
| Validation       | Pydantic v2               |
| Database         | MongoDB Atlas             |
| OCR              | PyTesseract, Pillow       |
| Document Parsing | PyPDF, python-docx        |
| Async Processing | asyncio                   |
| Email Service    | smtplib                   |
| Deployment       | Streamlit Community Cloud |

---

## 📂 Project Structure

```text
Resolvix_AI/
│
├── app.py
├── requirements.txt
├── README.md
│
├── data/
├── output/
│
└── src/
    ├── ingestion.py
    ├── extractor.py
    ├── generators.py
    ├── workflow.py
    ├── llm_handler.py
    ├── schema.py
    ├── db.py
    ├── email_sender.py
    ├── exporter.py
    └── logger.py
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/Radhika45/Resolvix_AI.git

cd Resolvix_AI
```

### Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```powershell
.\venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key

GROQ_MODEL=openai/gpt-oss-20b

OLLAMA_MODEL=llama3.2

MONGO_URI=your_mongodb_connection_string

DB_NAME=complaint_management_db

SMTP_SERVER=smtp.gmail.com

SMTP_PORT=587

SMTP_USERNAME=your_email@gmail.com

SMTP_PASSWORD=your_app_password
```

---

## 🚀 Run the Application

```bash
streamlit run app.py
```

Then open:

```text
http://localhost:8501
```

---

## 📊 Sample Output

### Extracted Complaint Data

```json
{
  "customer_name": "Sarah Connor",
  "email": "sarah.c@sky.net",
  "complaint_category": "Billing Error",
  "urgency_level": "High",
  "sentiment": "Frustrated",
  "summary": "Customer charged twice for subscription renewal."
}
```

---

## 🎯 Key Achievements

* Multi-format document ingestion
* Structured LLM extraction
* Automated customer communication
* Executive summary generation
* MongoDB persistence
* Async batch processing
* Streamlit analytics dashboard
* Cloud and local LLM support

---

## 🔮 Future Enhancements

* Retrieval-Augmented Generation (RAG)
* LangGraph-based agent workflows
* Docker containerization
* Role-Based Access Control (RBAC)
* Multi-language complaint processing
* Human-in-the-loop approvals

---

## 👩‍💻 Author

**Radhika**

B.Tech Computer Science & Engineering
PCTE Institute of Engineering & Technology

GitHub: https://github.com/Radhika45

---

## 📜 License

This project is licensed under the MIT License.
