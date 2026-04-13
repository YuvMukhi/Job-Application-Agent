import json
import requests
from bs4 import BeautifulSoup
import google.genai as genai
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

    # Call Gemini
    response = client.models.generate_content(
        model=config.GEMINI_MODEL,
        contents=prompt
    )
    result_text = response.text.strip()

    # Parse JSON (assuming it returns JSON)
    try:
        result = json.loads(result_text)
    except json.JSONDecodeError:
        # If not JSON, try to extract
        # For simplicity, assume it's JSON
        raise ValueError("Failed to parse JSON from response")

    return result