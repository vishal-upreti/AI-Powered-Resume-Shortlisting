# TalentLens — AI-Powered Resume Shortlisting (Midterm Prototype)

A local web application for comparing PDF/DOCX resumes with a job description. This first milestone demonstrates upload, text extraction, explainable NLP similarity, required-skill comparison, ranked results, search, and CSV export.

> **Important:** The score is a simple decision-support estimate, not a trained hiring model and not a definitive measure of candidate quality. A recruiter must review candidates individually. Do not use sensitive personal characteristics to rank applicants.

## 1. Features included now

- Responsive dashboard and job-description form.
- Multiple PDF and DOCX resumes (up to 10 per run; 16 MB total request limit).
- In-memory text extraction using PyMuPDF and python-docx. The app does not write resume files to an upload folder.
- TF-IDF + cosine similarity between role text and extracted resume text.
- Optional required-skill list and skill coverage calculation.
- Ranked results table, matched/missing skills, basic search, and CSV export.
- Basic validation and readable error messages.

### Matching score

When a required-skills list is provided:

`Final score = (0.65 × text similarity) + (0.35 × required-skill coverage)`

Without a required-skills list, final score is the text-similarity score. TF-IDF and cosine similarity are an explainable NLP baseline; they are not a trained machine-learning hiring model. Skill matching depends on text extraction and the words supplied by the recruiter.

## 2. Requirements

- Windows 10/11
- Python 3.11 or 3.12 recommended
- Internet connection only if installing packages for the first time

## 3. Run on Windows

1. Extract the project ZIP into a folder, for example `C:\Projects\resume_shortlisting_midterm`.
2. Open that folder in VS Code, or open Command Prompt in that folder.
3. Check Python:

   ```powershell
   py --version
   ```

4. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

5. Activate it in PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt instead and run:

   ```bat
   .venv\Scripts\activate.bat
   ```

6. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

7. Start the app:

   ```powershell
   python app.py
   ```

8. Open `http://127.0.0.1:5000` in your browser.
9. Enter a role and job description, add required skills separated by commas (for example `Python, SQL, Flask, Git`), upload 2–3 text-based PDF/DOCX resumes, and click **Analyze resumes**.

Press `Ctrl+C` in the terminal to stop the app.

## 4. Quick troubleshooting

- **`py` is not recognized:** Install Python from the official Python website and select the option to add Python to PATH, then reopen the terminal.
- **Package installation fails:** Check your internet connection and run `python -m pip install --upgrade pip`, then retry `pip install -r requirements.txt`.
- **No text extracted from a PDF:** The file may be a scanned image. This prototype handles text-based PDFs; OCR is not included in the midterm scope.
- **Scores look lower than expected:** Text similarity depends on how much wording overlaps. Try including concrete duties in the job description and a clear required-skill list.
- **Port 5000 is busy:** Stop the other app using it, or change the final `app.run(... port=5000 ...)` setting in `app.py` to `5001` and open `http://127.0.0.1:5001`.

## 5. Folder structure

```text
resume_shortlisting_midterm/
├── app.py                 # Flask routes, upload validation, resume text extraction
├── matcher.py             # TF-IDF similarity and skill coverage logic
├── requirements.txt       # Python dependencies
├── README.md              # Setup, usage, and troubleshooting
├── .gitignore
├── templates/
│   └── index.html         # Dashboard, form, and results template
└── static/
    ├── styles.css         # Responsive user interface
    └── app.js             # File picker, validation, search, CSV export
```

## 6. Current limitations / future milestones

- Analysis results are rendered for the current request; there is no persistent database or previous-analysis history yet.
- The app does not use a third-party paid AI service.
- A scanned PDF that contains only images will need OCR in a future milestone.
- The skill dictionary can be expanded and carefully tested.
- Authentication, production deployment hardening, automated tests, database-backed history, and advanced reporting are future enhancements.
- Before any real hiring use, assess data protection, security, accessibility, bias, and validity requirements with qualified guidance.
