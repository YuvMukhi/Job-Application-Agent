import json
import google.genai as genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

def tailor_resume(context):
    """Tailor the resume based on JD."""
    resume_text = json.dumps(context['resume'], indent=2)
    keywords = ', '.join(context['job_description']['keywords'])
    required_skills = ', '.join(context['job_description']['required_skills'])
    responsibilities = '; '.join(context['job_description']['responsibilities'])

    # Load prompt
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

    # Call Gemini
    response = client.models.generate_content(
        model=config.GEMINI_MODEL,
        contents=prompt
    )
    return response.text