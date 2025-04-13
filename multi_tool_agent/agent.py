import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from dotenv import load_dotenv
from google.adk.tools import google_search, agent_tool
from google.adk.agents import LlmAgent, BaseAgent


description_agent = LlmAgent(
    model="gemini-2.0-flash-exp", # Required: Specify the LLM 
    name="question_answer_agent", # Required: Unique agent name
    description="A helpful assistant agent that can answer questions. It should give more information to the children about the object they are intersted in. Make sure that you keep the responses short and simple. "
                "You can also use the google_search tool to find more information about the object. ",
    instruction="""Respond to the query using google search""",
    # google_search is a pre-built tool which allows the agent to perform Google searches.
    # tools=[google_search], # Provide an instance of the tool
)

def get_images():
    # This function should return a list of images or image URLs.
    # For the sake of this example, let's return an empty list.
    return []

image_recognizer_agent = LlmAgent(
    model="gemini-2.0-flash-exp",
    name="image_recognizer_agent",
    description="A helpful assistant agent that can recognize images using the function get_images. It should tell which is the most prominent object in the image that we have . Make sure that the output follows the format of 'color' 'object_name'. Do not give anything more as the output. in case of a particular flower it should use the google search and give the answer as 'color' 'flower_name'. do not add anything more to the output.", ,
    instruction="""Respond to the query using google search""",
    # google_search is a pre-built tool which allows the agent to perform Google searches.
    # tools=[google_search], # Provide an instance of the tool
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
    ],
    tools=[agent_tool.AgentTool(agent=description_agent)],

)


