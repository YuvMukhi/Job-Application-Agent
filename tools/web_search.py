from tavily import TavilyClient
import config

client = TavilyClient(api_key=config.TAVILY_API_KEY)

def search_web(query, max_results=3):
    """Perform a web search and return top results."""
    response = client.search(query=query, max_results=max_results)
    results = []
    for result in response['results']:
        results.append({
            'title': result['title'],
            'url': result['url'],
            'content': result['content']
        })
    return results