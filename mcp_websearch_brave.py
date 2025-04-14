import os
import json
import requests
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import uvicorn
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any, List

app = FastAPI(title="MCP Web Search Server")

class SearchRequest(BaseModel):
    query: str
    num_results: Optional[int] = 5

class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str

class SearchResponse(BaseModel):
    results: List[SearchResult]
    query: str

# You can use different search engines: DuckDuckGo, Brave, etc.
# This example uses a free method with Brave search
def brave_search(query: str, num_results: int = 5) -> List[Dict[str, str]]:
    """
    Perform a web search using Brave Search.
    """
    url = "https://search.brave.com/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    params = {"q": query}
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        search_results = []
        result_elements = soup.select('#results .snippet')
        
        for element in result_elements[:num_results]:
            title_element = element.select_one('.title')
            url_element = element.select_one('.url')
            description_element = element.select_one('.description')
            
            title = title_element.get_text() if title_element else "No title"
            url = url_element.get_text() if url_element else ""
            if not url and title_element and title_element.find('a'):
                url = title_element.find('a').get('href', "")
            snippet = description_element.get_text() if description_element else "No description available"
            
            search_results.append({
                "title": title,
                "url": url,
                "snippet": snippet
            })
        
        return search_results
    
    except Exception as e:
        print(f"Error performing search: {e}")
        return [{"title": "Error", "url": "", "snippet": f"Search failed: {str(e)}"}]

@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Endpoint to handle web search requests.
    """
    results = brave_search(request.query, request.num_results)
    return {"results": results, "query": request.query}

@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy", "service": "mcp-web-search"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)