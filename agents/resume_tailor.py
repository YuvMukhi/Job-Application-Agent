import json
from groq import Groq
import config

client = Groq(api_key=config.GROQ_API_KEY)

def tailor_resume(context):
    """Tailor the resume with improved summarization accuracy."""
    # Convert structured data to strings
    resume_json = json.dumps(context['resume'], indent=2)
    keywords = ', '.join(context['job_description']['keywords'])
    required_skills = ', '.join(context['job_description']['required_skills'])
    responsibilities = '; '.join(context['job_description']['responsibilities'])

    with open('prompts/tailor_prompt.txt', 'r') as f:
        prompt_template = f.read()

    # We add a specific instruction for the summary to be more descriptive
    instruction_overlay = (
        "\nCRITICAL: The 'Summary' section must be a professional narrative (3-4 sentences) "
        "highlighting specific years of experience and top technical achievements found in the resume."
    )

    prompt = prompt_template.format(
        job_title=context['job_description']['job_title'],
        company_name=context['job_description']['company_name'],
        resume_text=resume_json,
        keywords=keywords,
        required_skills=required_skills,
        responsibilities=responsibilities
    ) + instruction_overlay

    # Call Groq
    completion = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are an expert career coach and professional resume writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7 # Slight temperature increase helps for creative summary writing
    )
    
    return completion.choices[0].message.content