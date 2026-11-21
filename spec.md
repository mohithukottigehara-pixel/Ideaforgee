c# CIVICPROOF AI
## Software Requirements Specification (SRS) and Development Specification

**Project Title:** CivicProof AI: Intelligent Government Notification Lifecycle and Citizen Actionability Assistant  
**Document Type:** Product and Technical Specification  
**Version:** 1.0  
**Development Target:** Hackathon MVP  
**Primary Developer:** Individual Participant  
**Development Timeline:** 24 hours  
**Primary Programming Language:** Python

---

# 1. Project Overview

## 1.1 Purpose

CivicProof AI is an AI-powered platform designed to help citizens understand, verify, compare and act upon government notifications, circulars, policy documents and public announcements.

The system analyzes uploaded documents, extracts important information, compares them against a curated collection of official reference documents, identifies potential inconsistencies or outdated versions, and provides easy-to-understand explanations and personalized action checklists.

The primary objective is to transform complex government communications into reliable, understandable and actionable information.

## 1.2 Problem Statement

Citizens frequently receive government notifications through websites, messaging applications and social media. They often struggle to determine:

- Whether a notification matches an official government source.
- Whether the document is current or outdated.
- Whether an amendment or revised notification exists.
- Whether the notification applies to their circumstances.
- What deadlines and eligibility conditions are involved.
- What actions they need to take.

Existing systems may provide document access, translation or fact-checking independently. Citizens still need to manually connect this information.

CivicProof AI aims to simplify this process through a unified document analysis and citizen actionability workflow.

## 1.3 Proposed Solution

The application will allow users to upload a government notification in PDF format or paste its text.

The system will:

1. Extract text from the uploaded document.
2. Use an AI model to identify important notification details.
3. Compare the extracted information against a curated official reference database.
4. Identify possible mismatches, amendments and outdated versions.
5. Extract eligibility conditions, dates and deadlines.
6. Explain the notification in simple language.
7. Generate a citizen action checklist.
8. Display evidence and official reference links.
9. Support explanations in English, Kannada and Hindi.

---

# 2. Project Objectives

The application must achieve the following objectives:

- Improve accessibility of government information.
- Reduce confusion caused by outdated or inconsistent notifications.
- Simplify complex policy and administrative language.
- Identify potential document discrepancies.
- Help citizens understand eligibility requirements.
- Highlight important dates and deadlines.
- Generate actionable guidance based on document contents.
- Provide transparent explanations supported by document evidence.

---

# 3. Target Users

| User Category | Expected Benefit |
|---|---|
| Students | Understand scholarship notifications, application deadlines and eligibility |
| Farmers | Understand agricultural schemes and government announcements |
| Job Seekers | Understand recruitment notifications, qualifications and application dates |
| Senior Citizens | Understand welfare schemes and required documents |
| Small Business Owners | Understand registrations, subsidies and government policies |
| General Citizens | Understand public notices, circulars and administrative updates |

---

# 4. Technology Stack

Use the following technologies for the initial MVP.

| Component | Technology | Purpose |
|---|---|---|
| Programming Language | Python 3.11 or compatible version | Main application development |
| Frontend | Streamlit | User interface |
| AI Model | Google Gemini API using `google-genai` | Document understanding and explanations |
| PDF Processing | PyMuPDF or pypdf | Extract text from PDF documents |
| Data Processing | Pandas | Process structured information |
| Text Matching | RapidFuzz | Compare document text and metadata |
| Database | JSON initially, SQLite optionally | Store official reference documents |
| Charts | Plotly | Optional visual analytics |
| Environment Variables | python-dotenv / Streamlit Secrets | Secure API key management |
| Version Control | Git and GitHub | Source code management |
| Deployment | Streamlit Community Cloud | Application hosting |

**Development principle:** Prefer simple, maintainable Python modules. Do not introduce complex frameworks, microservices, multi-agent systems or unnecessary infrastructure.

---

# 5. Functional Requirements

## FR-01: Home Dashboard

The application must provide a professional landing page.

It should include:

- CivicProof AI logo and project name.
- Short description of the platform.
- Main document upload section.
- Document analysis instructions.
- Supported languages.
- Key feature cards.
- Clear disclaimer explaining the limitations of automated verification.

## FR-02: Document Upload

Users must be able to upload a government notification in PDF format.

Requirements:

- Accept PDF files.
- Validate the uploaded file type.
- Display the uploaded filename.
- Provide a document preview or extracted text preview.
- Display meaningful errors for invalid or empty files.
- Handle password-protected or unreadable PDFs gracefully.
- Limit upload size to a configurable maximum, initially 10 MB.

For the MVP, PDF upload and pasted text are mandatory.

Image upload and OCR are optional enhancements if time permits.

## FR-03: Document Text Extraction

The system must extract readable text from uploaded PDFs.

Extract the following where available:

- Document title.
- Issuing authority.
- Department name.
- Notification number.
- Publication date.
- Effective date.
- Eligibility conditions.
- Application deadline.
- Required documents.
- Benefits or provisions.
- Contact details.
- References to previous notifications.
- Amendment or supersession references.

If information is missing, return `null` or mark it as unavailable.

Never invent missing document information.

## FR-04: AI Document Analysis

Use the Gemini API to analyze the extracted document text.

The AI must return structured JSON containing:

- Document title.
- Issuing authority.
- Department.
- Notification number.
- Publication date.
- Effective date.
- Scheme or policy name.
- Eligibility criteria.
- Application deadline.
- Required documents.
- People affected.
- Main provisions.
- Citizen actions.
- Previous notification references.
- Possible amendment references.
- Important warnings.
- Source passages supporting extracted information.

The AI must distinguish between explicitly stated facts and inferred information.

All uncertain or unavailable fields must be clearly identified.

## FR-05: Official Source Verification

The system must compare uploaded documents against a locally curated collection of official reference documents.

The reference database must contain:

- Reference document ID.
- Document title.
- Department.
- Issuing authority.
- Notification number.
- Publication date.
- Effective date.
- Version.
- Extracted text or document content.
- Official source URL.
- Document status, where known.
- Related document IDs, where applicable.

### Verification statuses

The application must support four outcomes:

**1. Official Match**

The uploaded document sufficiently matches a specific curated official reference.

**2. Corroborated**

Some identifying details are supported by a reference, but the complete document has not been matched.

**3. Inconsistent**

A meaningful discrepancy exists between the uploaded document and a known official reference.

**4. Unverified**

No suitable official reference was found.

Important verification rules:

- Unverified does not mean fake.
- Inconsistent does not automatically mean fraudulent.
- A document may be genuine but absent from the curated database.
- The application must not claim that a document is authentic based only on its logo, formatting, signature or AI confidence.
- The application must show which official reference was used for comparison.
- The system must display the exact fields or passages that differ whenever possible.

The verification engine must use deterministic Python comparison logic. AI may assist with document understanding, but it must not independently decide authenticity.

## FR-06: Document Version Comparison

The application must compare an uploaded notification against relevant reference versions.

Compare:

- Notification number.
- Publication date.
- Effective date.
- Eligibility conditions.
- Application deadlines.
- Benefits and provisions.
- Required documents.
- Important instructions.

Display:

- Matching information.
- Changed information.
- Missing information.
- Newly introduced information.
- Potentially outdated information.

If the reference database does not contain multiple versions, clearly state that version history could not be established.

Do not claim that a document has been superseded unless a supporting official reference explicitly establishes that relationship.

## FR-07: Amendment and Supersession Detection

Identify possible references to:

- Previous notifications.
- Revised notifications.
- Amendments.
- Extensions.
- Withdrawals.
- Replacements.
- Superseded documents.

The application should distinguish between:

- An explicit amendment or supersession reference.
- A possible relationship requiring further verification.
- No related reference found.

## FR-08: Citizen Applicability Analysis

The application should help users understand whether a notification may apply to them.

For the MVP, collect only the minimum information required for a useful explanation.

Example fields:

- User category: Student, Farmer, Job Seeker, Senior Citizen, Business Owner or Other.
- State or region.
- Relevant eligibility information, if requested by the notification.

The system should compare these details with the notification's stated eligibility conditions.

Display one of the following:

- Appears eligible based on provided information.
- Appears potentially ineligible.
- More information is required.
- Eligibility cannot be determined from the available document.

The system must explain the reason behind the result.

Do not present AI-generated eligibility conclusions as official decisions.

## FR-09: Deadline and Important Date Extraction

Identify and display:

- Publication date.
- Effective date.
- Application opening date.
- Application closing date.
- Document submission deadline.
- Important event dates.

Display unavailable dates as "Not specified".

Highlight approaching or expired deadlines where the date can be reliably interpreted.

Avoid calculating deadline status when the source date or timezone is ambiguous.

## FR-10: Simple Language Explanation

Convert complex government language into simple explanations.

The explanation must include:

- What the notification is about.
- Who is affected.
- What benefits or provisions are available.
- Who may be eligible.
- Important dates.
- Required documents.
- What citizens should do next.

Keep explanations concise, understandable and organized.

Every important claim should be linked to a supporting document passage or official reference.

## FR-11: Multilingual Support

The application must support:

- English.
- Kannada.
- Hindi.

Users should be able to select their preferred explanation language.

The underlying extracted document content should remain available in its original language.

Translation must not change dates, amounts, eligibility conditions or official identifiers.

If translation is uncertain, the application should preserve the original text alongside the explanation.

## FR-12: Personalized Citizen Action Checklist

Generate an actionable checklist based on the notification.

Example:

- Read the eligibility conditions.
- Confirm the application deadline.
- Prepare the required documents.
- Visit the official application portal.
- Submit the application before the deadline.
- Save the application acknowledgement.

Checklist items must be derived from the document.

Do not generate unsupported application URLs or government procedures.

Allow users to mark checklist items as completed.

## FR-13: Evidence and Source References

For every important verification or explanation result, show:

- Source document name.
- Official reference URL, when available.
- Relevant document passage.
- Extracted field.
- Comparison result.

External links must point to actual source URLs stored in the reference database.

If a source URL is unavailable, display that no official link is available.

---

# 6. User Interface Specification

The interface should be modern, responsive, accessible and simple enough for non-technical citizens.

## 6.1 Visual Design

Suggested design direction:

- Primary color: Deep navy blue.
- Secondary color: Teal.
- Background: Light grey or off-white.
- Cards: White with subtle borders and rounded corners.
- Typography: Clean sans-serif font.
- Icons: Simple and consistent.
- Layout: Responsive and uncluttered.

Avoid excessive animations and decorative elements.

## 6.2 Main Navigation

Provide the following navigation sections:

1. Home
2. Analyze Document
3. Verify Document
4. Compare Versions
5. Citizen Assistant
6. About CivicProof

The MVP may implement these as sections or tabs within one Streamlit application.

## 6.3 Analysis Results Dashboard

After successful analysis, organize the results into the following sections:

**A. Document Overview**
- Document title.
- Issuing department.
- Notification number.
- Publication date.
- Effective date.

**B. Verification Result**
- Verification status.
- Matching reference.
- Comparison summary.
- Important discrepancies.

**C. Eligibility and Applicability**
- Target audience.
- Eligibility criteria.
- User-specific applicability result.

**D. Important Dates**
- Application opening date.
- Application deadline.
- Other relevant dates.

**E. Simple Explanation**
- Easy-to-understand summary.
- Key benefits.
- Important conditions.

**F. Action Checklist**
- Actionable steps.
- Completion checkboxes.

**G. Evidence and Sources**
- Supporting document passages.
- Official reference links.

---

# 7. Application Architecture

Use a modular architecture.

### Processing workflow

1. User uploads a PDF or pastes notification text.
2. Input validation checks the document.
3. PDF processing module extracts text.
4. AI analysis module extracts structured information.
5. Verification module searches the curated reference database.
6. Comparison module identifies discrepancies and version differences.
7. Applicability module evaluates user-provided information.
8. Citizen assistant generates a simplified explanation and checklist.
9. Streamlit displays the results with evidence and source references.

### Architecture principles

- Keep AI extraction separate from verification logic.
- Use deterministic Python rules for date, identifier and text comparisons.
- Never allow AI to invent official references.
- Keep all reference data traceable to its source.
- Handle API failures without crashing the application.
- Use session state carefully to preserve results during interaction.

---

# 8. Proposed Project Folder Structure

Create the following folder structure:

```text
CivicProof-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── modules/
│   ├── __init__.py
│   ├── document_reader.py
│   ├── ai_analyzer.py
│   ├── verification.py
│   ├── policy_compare.py
│   ├── citizen_assistant.py
│   └── utils.py
│
├── data/
│   ├── official_references.json
│   └── demo_documents/
│
├── assets/
│   └── logo.png
│
└── .streamlit/
    └── secrets.toml
```

Do not commit `.env` or `secrets.toml` containing API keys to GitHub.

---

# 9. Data Design

Use JSON for the initial reference database.

Example structure:

```json
[
  {
    "document_id": "DEMO001",
    "title": "Scholarship Notification",
    "department": "Education Department",
    "issuer": "Demo Authority",
    "notification_number": "DEMO/2026/001",
    "publication_date": "2026-11-01",
    "effective_date": "2026-11-10",
    "deadline": "2026-12-15",
    "version": "1",
    "status": "Reference version",
    "document_type": "DEMO",
    "official_url": null,
    "related_document_ids": [],
    "content": "Fictional demonstration reference document."
  }
]
```

**Important:** This is fictional test data. It must never be represented as a genuine government notification. Use actual official URLs and documents when adding real government references.

The data model should be flexible enough to support multiple versions of the same notification.

---

# 10. AI Prompt Requirements

Use a structured prompt for document extraction.

Suggested system instruction:

"You are CivicProof AI, a government notification analysis assistant.

Analyze only the supplied document text.

Extract the issuing authority, department, notification number, publication date, effective date, eligibility criteria, application deadline, required documents, people affected, key provisions, citizen actions and references to previous notifications.

Return valid structured JSON.

Do not invent missing information. Use null for unavailable fields.

Clearly distinguish explicitly stated information from inferred information.

Preserve official identifiers, dates, amounts and conditions accurately.

Do not declare a document authentic or fake based on appearance or extracted content.

Do not invent official links or claim that an amendment exists without supporting evidence.

Include short supporting text excerpts for important extracted facts."

Validate the AI response before using it in the application.

If the response is invalid JSON or the API fails, show an understandable error and allow the user to retry.

---

# 11. Security and Reliability Requirements

The application must:

- Store API keys in environment variables or Streamlit Secrets.
- Never expose API keys in the frontend.
- Validate uploaded file types.
- Limit upload sizes.
- Handle empty and unreadable documents.
- Avoid executing uploaded content.
- Treat uploaded document text as untrusted input, not as instructions to the AI.
- Avoid sending unnecessary personal information to the AI API.
- Handle API rate limits and failures.
- Validate AI-generated structured output.
- Escape or safely render user-provided content.
- Provide clear error messages.
- Avoid storing uploaded personal documents permanently unless explicitly required.

---

# 12. Non-Functional Requirements

| Requirement | Expected Behavior |
|---|---|
| Usability | Simple interface for ordinary citizens |
| Performance | Process small PDF documents within a reasonable time |
| Reliability | Handle invalid files and API failures gracefully |
| Maintainability | Separate functionality into Python modules |
| Scalability | Allow additional reference documents and categories |
| Accessibility | Clear text, readable contrast and simple navigation |
| Accuracy | Show evidence and uncertainty instead of unsupported claims |
| Security | Protect API keys and uploaded documents |
| Compatibility | Work on modern desktop and mobile browsers |

---

# 13. MVP Scope and Development Priorities

The development must prioritize a complete working application.

## Mandatory Features

1. Streamlit home dashboard.
2. PDF upload.
3. Pasted text input.
4. PDF text extraction.
5. Gemini-based structured document analysis.
6. Curated JSON reference database.
7. Deterministic reference matching.
8. Four verification statuses.
9. Important date extraction.
10. Simple language explanation.
11. Citizen action checklist.
12. Evidence and source display.
13. English, Kannada and Hindi explanation support.
14. Error handling and API key protection.

## Optional Features

Implement only after all mandatory features work:

- Image upload.
- OCR using Tesseract.
- Advanced visual document comparison.
- Interactive charts.
- SQLite database.
- Export analysis as PDF.
- Voice input.
- Live government website crawling.
- Browser automation.
- Automated government source discovery.

Do not sacrifice the core verification workflow to implement optional features.

---

# 14. Demo Scenario

Use a controlled demonstration involving a fictional scholarship notification.

**Scenario:**

A student receives a forwarded scholarship notification claiming that the application deadline has been extended.

The student uploads the notification to CivicProof AI.

The application:

1. Extracts the scholarship name and issuing authority.
2. Identifies the stated application deadline.
3. Finds a matching fictional reference document in its demonstration database.
4. Compares the two deadlines.
5. Identifies the discrepancy.
6. Displays an Inconsistent result.
7. Shows the conflicting dates and supporting passages.
8. Explains the issue in Kannada or English.
9. Generates a checklist advising the student to confirm the deadline using the official source.

Clearly label the demonstration documents as simulated.

Do not present the simulated scholarship or authority as a real government scheme.

---

# 15. Acceptance Criteria

The project is considered a successful MVP when the following tests pass.

| Test | Expected Result |
|---|---|
| Upload a valid PDF | File is accepted |
| Upload an invalid file | Clear validation message appears |
| Upload a scanned PDF without OCR support | Application explains that readable text could not be extracted |
| Paste notification text | Analysis begins successfully |
| Analyze a valid document | Structured fields are displayed |
| Match a curated reference | Official Match is displayed when matching rules are satisfied |
| Find partial metadata support | Corroborated is displayed |
| Detect a meaningful discrepancy | Inconsistent is displayed with evidence |
| Find no reference | Unverified is displayed |
| Extract a deadline | Date is displayed accurately |
| Missing deadline | Not specified is displayed |
| Change explanation language | Explanation is translated |
| Generate checklist | Actionable items are displayed |
| Gemini API failure | Application does not crash |
| Missing API key | Clear configuration instructions appear |
| No official reference URL | Application does not invent a link |
| No version history | Application does not claim supersession |

---

# 16. Development Timeline

Target total development time: 24 hours.

| Time | Development Task |
|---|---|
| Hours 0–2 | Environment setup, dependencies and API configuration |
| Hours 2–5 | Streamlit interface and PDF upload |
| Hours 5–8 | PDF text extraction and validation |
| Hours 8–11 | Gemini document analysis |
| Hours 11–14 | JSON reference database and verification engine |
| Hours 14–16 | Document comparison and discrepancy detection |
| Hours 16–18 | Citizen explanation and action checklist |
| Hours 18–19 | Multilingual support |
| Hours 19–21 | Testing, error handling and UI improvements |
| Hours 21–22 | Deployment |
| Hours 22–24 | Final debugging, demonstration and presentation preparation |

If time becomes limited, prioritize the complete PDF-to-analysis-to-verification-to-action-checklist workflow.

---

# 17. Instructions for Codex

Act as a senior Python developer and build the CivicProof AI application according to this specification.

Follow these development instructions strictly:

1. Create the complete project folder structure.
2. Use Python and Streamlit.
3. Use the Gemini API through the official `google-genai` package.
4. Build a functional application, not just a frontend mockup.
5. Implement PDF text extraction and pasted-text analysis.
6. Implement structured AI extraction with JSON validation.
7. Implement a deterministic verification engine using the curated JSON reference database.
8. Support the four verification statuses defined in this specification.
9. Implement document comparison, date extraction and discrepancy reporting.
10. Implement simple explanations and citizen action checklists.
11. Support English, Kannada and Hindi explanations.
12. Include clear error handling and API key protection.
13. Use sample fictional documents only for demonstration and label them clearly.
14. Do not fabricate government sources, official URLs or notification details.
15. Keep the interface modern, professional, responsive and easy to navigate.
16. Avoid unnecessary dependencies and complicated architecture.
17. Write clean, modular, commented code suitable for a beginner to understand.
18. Include `requirements.txt`, `.env.example`, `.gitignore` and a detailed README.
19. Include instructions for installing dependencies, configuring the API key, running locally and deploying.
20. Test the complete application workflow before declaring development complete.

### Coding workflow

Build the project in stages:

**Stage 1:** Project structure, dependencies and working Streamlit dashboard.

**Stage 2:** PDF upload, pasted text and document extraction.

**Stage 3:** Gemini integration and structured document analysis.

**Stage 4:** Reference database and deterministic verification engine.

**Stage 5:** Document comparison and discrepancy detection.

**Stage 6:** Citizen explanation, multilingual support and action checklist.

**Stage 7:** Testing, error handling and deployment preparation.

After each stage:

- Explain which files were created or modified.
- Explain how to run and test the functionality.
- Resolve errors before proceeding.
- Preserve working functionality from previous stages.

Do not stop after creating placeholder files. Implement the actual functionality.

If an API key or external configuration is unavailable, build the remaining application and provide clear setup instructions.

### Final deliverables

The completed project must contain:

- Fully functional CivicProof AI source code.
- Complete project folder structure.
- Requirements file.
- Environment configuration example.
- Sample demonstration documents.
- Sample reference database.
- README with setup instructions.
- Working local application.
- Deployment instructions.
- Test results for the mandatory acceptance criteria.

**Final instruction:** Build a reliable, demonstrable MVP first. Prioritize evidence-based document verification and citizen actionability over visual effects or advanced AI features.