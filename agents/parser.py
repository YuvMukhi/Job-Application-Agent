import json
import requests
import time
from bs4 import BeautifulSoup
import google.genai as genai
from google.api_core import exceptions
import config
from tools.pdf_reader import extract_text_from_file

client = genai.Client(api_key=config.GEMINI_API_KEY)

def parse_resume_and_jd(resume_path, jd_input):
    """Parse resume and job description into structured data."""
    # Extract resume text
    if resume_path.endswith(('.pdf', '.docx')):
        resume_text = extract_text_from_file(resume_path)
    else:
        with open(resume_path, 'r') as f:
            resume_text = f.read()

    # Extract JD text
    if jd_input.startswith('http'):
        response = requests.get(jd_input)
        soup = BeautifulSoup(response.text, 'html.parser')
        jd_text = soup.get_text()
    else:
        jd_text = jd_input

    # Load prompt
    with open('prompts/parse_prompt.txt', 'r') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(resume_text=resume_text, jd_text=jd_text)

    # Call Gemini with Retry Logic
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model=config.GEMINI_MODEL,
                contents=prompt
            )
            result_text = response.text.strip()
            
            # Clean up potential markdown formatting if present
            if result_text.startswith("```json"):
                result_text = result_text.replace("```json", "").replace("```", "").strip()

            return json.loads(result_text)

        except (exceptions.ServiceUnavailable, exceptions.InternalServerError):
            if attempt < 2:
                time.sleep(5)  # Wait 5 seconds before retrying
                continue
            raise
        except json.JSONDecodeError:
            raise ValueError("Failed to parse valid JSON from the AI response.")