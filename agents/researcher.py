from groq import Groq
import config
from tools.web_search import search_web

client = Groq(api_key=config.GROQ_API_KEY)

def research_company(company_name, job_title):
    """Research company and return a brief."""
    queries = [
        f"{company_name} mission and values",
        f"{company_name} tech stack",
        f"{company_name} recent news 2024 2025"
    ]

    all_snippets = []
    for query in queries:
        try:
            results = search_web(query, max_results=2)
            for result in results:
                all_snippets.append(result['content'])
        except Exception:
            continue

    research_snippets = "\n\n".join(all_snippets)

    with open('prompts/research_prompt.txt', 'r') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(company_name=company_name, job_title=job_title, research_snippets=research_snippets)

    completion = client.chat.completions.create(
        model=config.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content