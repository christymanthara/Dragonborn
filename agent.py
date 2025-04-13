import os
import requests
import json
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.llms import Ollama
from langchain import hub
from langchain_core.tools import Tool

# --- Configuration ---
OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "llama3"
MCP_SERVER_URL = "http://localhost:8000"  # Change if your MCP server runs on a different port

# --- Define Web Search Tool ---
def web_search(query: str) -> str:
    """
    Perform a web search to find information online.
    """
    try:
        response = requests.post(
            f"{MCP_SERVER_URL}/search",
            json={"query": query, "num_results": 3}
        )
        response.raise_for_status()
        
        data = response.json()
        results = data.get("results", [])
        
        if not results:
            return "No search results found."
        
        # Format the results
        formatted_results = f"Search results for '{query}':\n\n"
        for i, result in enumerate(results, 1):
            formatted_results += f"{i}. {result['title']}\n"
            formatted_results += f"   URL: {result['url']}\n"
            formatted_results += f"   {result['snippet']}\n\n"
        
        return formatted_results
    
    except Exception as e:
        return f"Error performing web search: {str(e)}"

# --- Define Tools ---
tools = [
    Tool(
        name="WebSearch",
        func=web_search,
        description="Search the web for current information. Use this when you need to find up-to-date facts, news, or information that might not be in your training data. Input should be a search query."
    )
]

# --- Initialize the LLM ---
try:
    llm = Ollama(model=MODEL_NAME, base_url=OLLAMA_BASE_URL)
    # Test connection
    llm.invoke("Test prompt")
    print(f"Successfully connected to Ollama model: {MODEL_NAME} at {OLLAMA_BASE_URL}")
except Exception as e:
    print(f"Error connecting to Ollama: {e}")
    print(f"Please ensure Ollama is running and the model '{MODEL_NAME}' is available.")
    print(f"You can pull models using: ollama pull {MODEL_NAME}")
    exit()

# --- Load the Agent Prompt ---
prompt = hub.pull("hwchase17/react")

# --- Create the Agent ---
agent = create_react_agent(llm, tools, prompt)

# --- Create the Agent Executor ---
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# --- Run the Agent ---
if __name__ == "__main__":
    print("LangChain Agent with Ollama and Web Search initialized.")
    print("MCP Server should be running at:", MCP_SERVER_URL)
    
    # Check if MCP server is available
    try:
        health_check = requests.get(f"{MCP_SERVER_URL}/health")
        if health_check.status_code == 200:
            print("✅ MCP Server is available and healthy")
        else:
            print("⚠️ MCP Server returned unexpected status:", health_check.status_code)
    except:
        print("⚠️ Could not connect to MCP Server. Make sure it's running!")
    
    print("\nAsk a question (or type 'exit' to quit):")
    while True:
        user_input = input("> ")
        if user_input.lower() == 'exit':
            break
        try:
            response = agent_executor.invoke({"input": user_input})
            print("\nAgent Response:")
            print(response['output'])
            print("-" * 30)
        except Exception as e:
            print(f"An error occurred: {e}")

    print("Exiting agent.")