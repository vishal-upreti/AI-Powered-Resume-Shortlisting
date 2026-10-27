# Midterm Demo Test Checklist

Use only sample resumes or resumes whose owners have given permission. Do not present the expected results as actual results until you run each test.

- [ ] App starts with `python app.py` and opens at `http://127.0.0.1:5000`.
- [ ] Submitting with an empty job title shows a validation message.
- [ ] Submitting with an empty job description shows a validation message.
- [ ] Submitting without a resume shows a validation message.
- [ ] A text-based PDF resume is read successfully.
- [ ] A DOCX resume is read successfully.
- [ ] An unsupported file type is rejected.
- [ ] A scanned/image-only PDF is handled with a useful message.
- [ ] Multiple resumes are ranked by their calculated scores.
- [ ] Required skills show both matched and missing skills.
- [ ] Candidate search filters the results table.
- [ ] CSV export downloads the visible results.
- [ ] App is stopped using `Ctrl+C`.

## Viva explanation

- **Flask:** Python web framework that receives form submissions and returns the web page.
- **PyMuPDF / python-docx:** Read text from PDF / DOCX files.
- **TF-IDF:** Weights words based on their importance in the job description and resume documents.
- **Cosine similarity:** Estimates similarity between the TF-IDF vectors.
- **Skill coverage:** Matched required skills divided by the total required skills.
- **Limit:** A textual match score cannot establish overall candidate quality and should not make hiring decisions on its own.
