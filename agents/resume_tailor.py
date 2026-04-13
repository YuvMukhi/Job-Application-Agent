import json
from groq import Groq
import config

client = Groq(api_key=config.GROQ_API_KEY)

def tailor_resume(context):
    resume_text = json.dumps(context['resume'], indent=2)
    keywords = ', '.join(context['job_description']['keywords'])
    required_skills = ', '.join(context['job_description']['required_skills'])
    responsibilities = '; '.join(context['job_description']['responsibilities'])

    with open('prompts/tailor_prompt.txt', 'r') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(
        job_title=context['job_description']['job_title'],
        company_name=context['job_description']['company_name'],
        resume_text=resume_text,
        keywords=keywords,
        required_skills=required_skills,
        responsibilities=responsibilities
    )

    completion = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content