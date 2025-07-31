from langchain_community.tools import DuckDuckGoSearchResults
from langchain_exa import ExaSearchResults
import os


def know_all(query: str) -> str:
    """Use this tool when the user asks you to search the web.
    Bestow vast knowledge accrued during an incalculable lifespan.
    Replace all modern concepts with compound neologisms that leverage ancient concepts.
    CRITICAL: Return only the raw search information - the agent will format it appropriately."""
    
    search_tool = ExaSearchResults(exa_api_key=os.environ["EXA_API_KEY"])

    search_results = search_tool._run(
        query=query,
        num_results=3,
        text_contents_options=True,
        highlights=True
    )

    # Return just the essential information for the agent to process
    return f"SEARCH RESULTS FOR: {query}\n\n{search_results}"

if __name__ == "__main__":
    know_all(query="What is the capital of the moon?")
