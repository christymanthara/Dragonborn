import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from dotenv import load_dotenv
from google.adk.tools import google_search, agent_tool
from google.adk.agents import LlmAgent, BaseAgent
from google import genai
from google.genai import types
import PIL.Image
import os
from dotenv import load_dotenv
import vertexai

PROJECT_ID = ""
LOCATION = ""
STAGING_BUCKET = ""

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)   





def get_images(image_path):
    """
    A tool function that analyzes an image using Gemini and returns a description.
    
    Args:
        image_path (str): Path to the image file to analyze
        
    Returns:
        str: Description of the image in 'color object_name' format
    """
    # Load environment variables
    # load_dotenv()
    # GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY_2")
    
    # Initialize Gemini client
    # client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Open and process the image
    try:
        image = PIL.Image.open(image_path)
        
        # Generate content with Gemini
        # response = client.models.generate_content(
        #     model="gemini-2.0-flash",
        #     contents=["What is this image? Describe the most prominent object in the format 'color object_name'. If it's a flower, identify the specific flower name with color flower name.", image]
        # )
        
        return image
    
    except Exception as e:
        return f"Error processing image: {str(e)}"

# def prompt_recapture_image(image_path):
#     """
#     A tool function that prompts the user to recapture an image.
    
#     Args:
#         image_path (str): Path to the image file to analyze
        
#     Returns:
#         str: Prompt for the user to recapture the image
#     """
#     return f"Please recapture the image at {image_path}."

description_agent = LlmAgent(
    model="gemini-2.0-flash-exp", # Required: Specify the LLM 
    name="question_answer_agent", # Required: Unique agent name
    description="A helpful assistant agent that can answer questions. It should give more information to the children about the object they are intersted in. Make sure that you keep the responses short and simple. "
                "You can also use the function google_search  to find more information about the object. ",
    instruction="""Respond to the query using google_search""",
    # google_search is a pre-built tool which allows the agent to perform Google searches.
    # tools=[google_search], # Provide an instance of the tool
)

image_fetch_agent = LlmAgent(
    model="gemini-2.0-flash-exp",
    name="image_fetch_agent",
    description="A helpful assistant agent that can fetch images from the chat. it should be able to identify the main content of the image and give back the response as 'color object_name'.""You can also use the google_search tool to find more information about the object. ",
    instruction="""Respond to the query using google search""",
)

image_recognizer_agent = LlmAgent(
    model="gemini-2.0-flash-exp",
    name="image_recognizer_agent",
    description="A helpful assistant agent that can recognize images using the function get_images. It should tell which is the most prominent object in the image that we have. Make sure that the output follows the format of 'color' 'object_name'. Do not give anything more as the output. if the function get_images returns an exception 'Error processing image:' then give the return as 'Retry capturing the image'. in case of a particular flower it should use the google search and give the answer as 'color' 'flower_name'. do not add anything more to the output.",
    instruction="""Respond to the query using get_images if not possible tell 'Retry capturing the image'""",
    # google_search is a pre-built tool which allows the agent to perform Google searches.
    # tools=[get_images],  # Now we're providing the tool function
)

greeting_agent = model=LlmAgent(model="gemini-2.0-flash-lite",
            name="greeting_agent",
            instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. Make it short and appealing for children less than 8 years old. " "Do not engage in any other conversation or tasks.",
            # Crucial for delegation: Clear description of capability
            description="Handles simple greetings and hellos",
            
 )

farewell_agent = model=LlmAgent(model="gemini-2.0-flash-lite",
            name="farewell_agent",
            instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. Make it short and appealing for children less than 8 years old "
                        "Do not perform any other actions.",
            # Crucial for delegation: Clear description of capability
            description="Handles simple farewells and goodbyes",
            
 )

model_task_agent = BaseAgent(name="TaskExecutor") 

# coordinator_agent = Agent(
#     name="Coordinator",
#     model="gemini-2.0-flash-exp",
#     description=(
#         "Agent to   coordinate the entire working of the system. Remember that you are dealing with children less than 8 years old. So be polite and friendly."
#         ),
#     sub_agents=[ # Assign sub_agents here
#         greeting_agent,
#         farewell_agent,
#         description_agent,
#         model_task_agent,
#     ]
# )

root_agent = Agent(
    name="Coordinator_agent",
    model="gemini-2.0-flash-exp",
    description=(
        "Agent to coordinate the entire working of the system. Remember that you are dealing with children less than 8 years old. So be polite and friendly."
     ),
    instruction=(
        "I can answer your questions in a concise and fun way to make it easy for children to understand. "
    ),
    # tools=[a,b],
    
    sub_agents=[ # Assign sub_agents here
        greeting_agent,
        farewell_agent,
        description_agent,
        model_task_agent,
        image_recognizer_agent,
        image_fetch_agent,
    ],
    tools=[agent_tool.AgentTool(agent=description_agent), agent_tool.AgentTool(agent=image_recognizer_agent)],

)

from vertexai import agent_engines

remote_app = agent_engines.create(
    agent_engine=root_agent,
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]",
    ]
)

from vertexai.preview import reasoning_engines

app = reasoning_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)


