from groq import Groq
import config

client = Groq(api_key=config.GROQ_API_KEY)

def write_cover_letter(context):
    with open('prompts/cover_letter_prompt.txt', 'r') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(
        candidate_name=context['resume']['name'],
        job_title=context['job_description']['job_title'],
        company_name=context['job_description']['company_name'],
        company_brief=context['company_brief'],
        tailored_resume=context['tailored_resume'],
        responsibilities='; '.join(context['job_description']['responsibilities'])
    )

    completion = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content