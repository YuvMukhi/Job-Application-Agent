import json
import requests
import time
from bs4 import BeautifulSoup
from groq import Groq
import config
from tools.pdf_reader import extract_text_from_file

client = Groq(api_key=config.GROQ_API_KEY)

def parse_resume_and_jd(resume_path, jd_input):
    """Parse resume and job description into structured data."""
    if resume_path.endswith(('.pdf', '.docx')):
        resume_text = extract_text_from_file(resume_path)
    else:
        with open(resume_path, 'r') as f:
            resume_text = f.read()

    if jd_input.startswith('http'):
        response = requests.get(jd_input)
        soup = BeautifulSoup(response.text, 'html.parser')
        jd_text = soup.get_text()
    else:
        jd_text = jd_input

    with open('prompts/parse_prompt.txt', 'r') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(resume_text=resume_text, jd_text=jd_text)

    # Groq API Call
    completion = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"} # Groq supports JSON mode
    )
    
    result_text = completion.choices[0].message.content
    return json.loads(result_text)