
from ddgs import DDGS


def search_web(query: str, max_results: int = 5):
    query = query.strip()

    if not query:
        raise ValueError("Search query cannot be empty")

    max_results = max(1, min(max_results, 5))

    try:
        results = DDGS(timeout=10).text(
            query,
            max_results=max_results
        )

        sources = []

        for result in results:
            sources.append({
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "snippet": result.get("body", "")
            })

        return sources

    except Exception as error:
        raise RuntimeError(
            f"Web search failed: {error}"
        ) from error
