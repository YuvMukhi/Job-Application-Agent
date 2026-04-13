import google.genai as genai
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)

def write_cover_letter(context):
    """Write the cover letter."""
    candidate_name = context['resume']['name']
    job_title = context['job_description']['job_title']
    company_name = context['job_description']['company_name']
    company_brief = context['company_brief']
    tailored_resume = context['tailored_resume']
    responsibilities = '; '.join(context['job_description']['responsibilities'])

    # Load prompt
    with open('prompts/cover_letter_prompt.txt', 'r') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(
        candidate_name=candidate_name,
        job_title=job_title,
        company_name=company_name,
        company_brief=company_brief,
        tailored_resume=tailored_resume,
        responsibilities=responsibilities
    )

    # Call Gemini
    response = client.models.generate_content(
        model=config.GEMINI_MODEL,
        contents=prompt
    )
    return response.text