# PII Masking Gateway

An AI-powered API Gateway that detects, classifies, and masks Personally Identifiable Information (PII) in HTTP requests before forwarding them to backend applications. The project also includes a Streamlit dashboard for real-time monitoring of detected PII incidents.

## Features

- Detects sensitive PII from incoming requests
- Automatically masks confidential information
- Assigns risk levels to detected data
- Logs PII incidents for auditing
- Real-time monitoring dashboard using Streamlit
- Works as a middleware between client applications and backend services

## Tech Stack

- Python
- FastAPI
- Streamlit
- Regex-based PII Detection
- JSON Logging
- Node.js (OWASP Juice Shop for demonstration)

## Project Structure

```
PII-Masking-Gateway/
│
├── gateway/
├── admin_dashboard/
├── frontend_streamlit/
└── README.md
```
