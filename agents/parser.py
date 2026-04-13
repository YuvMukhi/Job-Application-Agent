import json
import requests
import time
import re
from bs4 import BeautifulSoup
from groq import Groq
import config
from tools.pdf_reader import extract_text_from_file

client = Groq(api_key=config.GROQ_API_KEY)

def parse_resume_and_jd(resume_path, jd_input):
    """Parse resume and job description into structured data with verification logic."""
    # 1. Extract and sanitize resume text
    if resume_path.endswith(('.pdf', '.docx')):
        resume_text = extract_text_from_file(resume_path)
    else:
        with open(resume_path, 'r') as f:
            resume_text = f.read()
    
    # Simple sanitization to remove excessive whitespace
    resume_text = re.sub(r'\s+', ' ', resume_text).strip()

    # 2. Extract JD text
    if jd_input.startswith('http'):
        response = requests.get(jd_input)
        soup = BeautifulSoup(response.text, 'html.parser')
        jd_text = soup.get_text()
    else:
        jd_text = jd_input
    
    jd_text = re.sub(r'\s+', ' ', jd_text).strip()

    # 3. Initial Extraction Pass
    with open('prompts/parse_prompt.txt', 'r') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(resume_text=resume_text, jd_text=jd_text)

    completion = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are a precise data extraction expert. Return only valid JSON."},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"}
    )
    
    result = json.loads(completion.choices[0].message.content)

    # 4. Verification Pass: If Company Name is missing or generic
    current_company = result.get('job_description', {}).get('company_name', '').lower()
    if not current_company or any(x in current_company for x in ['unknown', 'string', 'company name']):
        # Focus on the beginning of the JD where the company name usually appears
        focused_text = jd_text[:1000]
        verify_prompt = f"Identify the hiring company name from this text. Return ONLY the name: {focused_text}"
        
        verify_call = client.chat.completions.create(
            model=config.GROQ_MODEL,
            messages=[{"role": "user", "content": verify_prompt}]
        )
        found_name = verify_call.choices[0].message.content.strip()
        result['job_description']['company_name'] = found_name

    return result