# Job Application Agent

An AI-powered agent that automates the job application process by parsing resumes and job descriptions, researching companies, tailoring resumes, writing cover letters, and packaging outputs.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up API keys in `.env`:
   - Get Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Get Tavily API key from https://tavily.com/
   - Replace the placeholders in `.env` with your actual keys.

3. The project is configured to use `gemini-2.5-flash` for all model calls.

4. Run the web application:
   ```
   python web.py
   ```
   Then open http://127.0.0.1:5000 in your browser.

## Features

- Upload resume in PDF, DOCX, or TXT format
- Enter job description as text or URL
- AI-powered company research
- Resume tailoring
- Cover letter generation
- Download generated documents

## Project Structure

- `web.py`: Flask web application
- `agents/`: Individual agent modules
- `tools/`: Utility tools
- `prompts/`: LLM prompts
- `outputs/`: Generated files
- `templates/`: HTML templates
- `static/`: CSS and JS files

## Phases

1. Parse resume and JD
2. Research company
3. Tailor resume
4. Write cover letter
5. Package outputs