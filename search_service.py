import openai_service

try:
    import web  # OpenAI environment only
except ImportError:
    web = None


def search_and_summarize(query: str) -> str:
    try:
        if web is None:
            return f"(로컬 환경에서는 웹 검색이 불가능합니다) — 검색어: {query}"
        # Perform a web search using the web tool
        search_results = web.search(query)
        if not search_results:
            return "No results found for your query."
        
        # Concatenate snippets or titles from search results for summarization
        combined_text = " ".join(result.get('snippet', '') for result in search_results if 'snippet' in result)
        if not combined_text:
            combined_text = " ".join(result.get('title', '') for result in search_results if 'title' in result)
        
        # Use openai_service to summarize the combined text
        summary = openai_service.summarize_text(combined_text)
        return summary
    except Exception as e:
        return f"An error occurred during search and summarization: {str(e)}"
