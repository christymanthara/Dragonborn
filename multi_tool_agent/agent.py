import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from dotenv import load_dotenv
import os

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

import requests
import json

def get_flower_info(flower_name:str) -> dict:
    """
    Get detailed information about a flower using Plant.id API
    
    Args:
        flower_name: The name of the flower identified by YOLOv8
        
    Returns:
        Dictionary with detailed information about the flower
    """
    # Replace with your Plant.id API key

    flower_id = os.getenv("plant_id_key")
    flower_api_key = flower_id
    
    # API endpoint for plant details
    url = f"https://plant.id/api/v2/species-info?key={flower_api_key}"
    
    # Prepare the request data
    data = {
        "name": flower_name
    }
    
    # Make the API request
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to get information: {response.status_code}"}

root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash-exp",
    description=(
        "Agent to answer questions about the time and weather in a city and also flower information using Plant.id API."
    ),
    instruction=(
        "I can answer your questions about the time and weather in a city. Also more information about flowers using Plant.id API. "
    ),
    tools=[get_weather, get_current_time, get_flower_info],

)


