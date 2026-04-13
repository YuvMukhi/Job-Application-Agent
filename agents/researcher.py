import google.genai as genai
import config
from tools.web_search import search_web

client = genai.Client(api_key=config.GEMINI_API_KEY)

def research_company(company_name, job_title):
    """Research company and return a brief."""
    queries = [
        f"{company_name} mission and values",
        f"{company_name} engineering culture" if "engineer" in job_title.lower() else f"{company_name} team culture",
        f"{company_name} tech stack",
        f"{company_name} recent news 2024 2025",
        f"{company_name} {job_title} team"
    ]

    all_snippets = []
    for query in queries:
        results = search_web(query, max_results=3)
        for result in results:
            all_snippets.append(result['content'])

    research_snippets = "\n\n".join(all_snippets)

    # Load prompt
    with open('prompts/research_prompt.txt', 'r') as f:
        prompt_template = f.read()

    prompt = prompt_template.format(company_name=company_name, job_title=job_title, research_snippets=research_snippets)

    # Call Gemini
    response = client.models.generate_content(
        model=config.GEMINI_MODEL,
        contents=prompt
    )
    return response.text