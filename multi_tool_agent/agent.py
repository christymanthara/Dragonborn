import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from dotenv import load_dotenv
from google.adk.tools import google_search
from google.adk.agents import LlmAgent, BaseAgent



def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (41 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (
                f"Sorry, I don't have timezone information for {city}."
            ),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}

description_agent = LlmAgent(
    model="gemini-2.0-flash-exp", # Required: Specify the LLM 
    name="question_answer_agent", # Requdired: Unique agent name
    description="A helpful assistant agent that can answer questions. It should give more information to the children about the object they are intersted in. Make sure that you keep the responses short and simple. "
                "You can also use the google search tool to find more information about the object. ",
    instruction="""Respond to the query using google search""",
    tools=[google_search], # Provide an instance of the tool
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
    name="weather_time_agent",
    model="gemini-2.0-flash-exp",
    description=(
        "Agent to answer questions about the time and weather in a city and also flower information using Plant.id API."
    ),
    instruction=(
        "I can answer your questions about the time and weather in a city. Also more information about flowers using Plant.id API. "
    ),
    tools=[get_weather, get_current_time],
    sub_agents=[ # Assign sub_agents here
        greeting_agent,
        farewell_agent,
        description_agent,
        model_task_agent,
    ],

)


