import os
from langchain.agents import AgentExecutor, create_react_agent
from langchain_community.llms import Ollama # Placeholder, will explain connection later
from langchain import hub
from langchain_core.tools import Tool

# --- Configuration ---
# Ensure you have Ollama running locally.
# By default, Ollama runs on http://localhost:11434
# Specify the model you want to use (e.g., "llama3", "mistral")
# Make sure the model is pulled in Ollama: `ollama pull llama3`
OLLAMA_BASE_URL = "http://localhost:11434"
MODEL_NAME = "llama3" # Replace with your desired Ollama model

# --- Define Tools (Example) ---
# Agents use tools to interact with the world or perform specific tasks.
# Here's a simple example tool. Replace or add tools as needed.
def simple_search(query: str) -> str:
    """A simple search tool that returns a fixed string."""
    print(f"--- Searching for: {query} ---")
    # In a real scenario, this would interact with a search engine API, database, etc.
    return f"Search results for '{query}': Found relevant information."

tools = [
    Tool(
        name="SimpleSearch",
        func=simple_search,
        description="Useful for when you need to answer questions about current events or general knowledge. Input should be a search query.",
    )
]

# --- Initialize the LLM ---
# We'll use Ollama. Ensure the Ollama service is running.
try:
    llm = Ollama(model=MODEL_NAME, base_url=OLLAMA_BASE_URL)
    # Test connection
    llm.invoke("Test prompt")
    print(f"Successfully connected to Ollama model: {MODEL_NAME} at {OLLAMA_BASE_URL}")
except Exception as e:
    print(f"Error connecting to Ollama: {e}")
    print(f"Please ensure Ollama is running and the model '{MODEL_NAME}' is available.")
    print(f"You can pull models using: ollama pull {MODEL_NAME}")
    exit() # Exit if connection fails

# --- Load the Agent Prompt ---
# We use a predefined prompt template from Langchain Hub for the ReAct agent.
# You can explore other prompts or create your own.
prompt = hub.pull("hwchase17/react")

# --- Create the Agent ---
# This binds the LLM, tools, and prompt together.
agent = create_react_agent(llm, tools, prompt)

# --- Create the Agent Executor ---
# This runs the agent loop (Thought, Action, Observation).
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True) # Set verbose=True to see the agent's thought process

# --- Run the Agent ---
if __name__ == "__main__":
    print("LangChain Agent with Ollama Initialized.")
    print("Ask a question (or type 'exit' to quit):")
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