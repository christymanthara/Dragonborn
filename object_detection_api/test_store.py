# Use google.cloud.aiplatform for initialization if needed elsewhere,
# but google-genai client handles it for generate_content when vertexai=True
# import vertexai
# vertexai.init(
#   project="clever-axe-456700-a1",
#   location="us-central1",
# )

# ExampleStore is not needed for basic function calling definition
# from vertexai.preview import example_stores
# example_store = example_stores.ExampleStore.create(
#     example_store_config=example_stores.ExampleStoreConfig(
#         vertex_embedding_model="text-embedding-005" # Embedding model might differ
#     )
# )

# from google.generativeai import types as genai_types
# from google.generativeai.types import Part # Correctly import Part
from google import genai
from google.genai import types as genai_types # Importing types from google.genai
# import genai.types.Parts  as Part # For clarity, use genai_types instead of importing Part directly
# import google.genai.types.Part as Part # Importing Parts from genai.types

import vertexai
from vertexai.generative_models import GenerativeModel
# vertexai.init(project="clever-axe-456700-a1", location="us-central1")

client = genai.Client(
    vertexai=True, project="clever-axe-456700-a1", location="us-central1"
)

# Now use the model
response = client.models.compute_tokens(
    model='gemini-2.0-flash',
    contents='What is your name?',
)
print(response)

# 1. Define the function declaration
get_current_weather_func = genai_types.FunctionDeclaration(
  name="get_current_weather",
  description="Get the current weather in a given location",
  parameters={
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "The city name of the location for which to get the weather, e.g. Boston"
      }
    },
    "required": ["location"] # Good practice to specify required parameters
  },
)

# 2. Initialize the google-genai Client for Vertex AI
#    Ensure your environment is authenticated (e.g., using gcloud auth application-default login)
client = genai.Client(
    # http_options=genai_types.HttpOptions(api_version="v1"), # Usually not needed
    vertexai=True,
    project="clever-axe-456700-a1",
    location="us-central1"
)

# 3. Prepare the user prompt
user_content = genai_types.Content(
    role="user",  # Explicitly setting the role to 'user'
    parts=[       # 'parts' is a list...
        genai_types.Part(text="What is the weather like in Boston?") # ...containing one Part object with the text content
    ]
)

# 4. Call the model with the function definition
#    Use a valid Vertex AI model name supporting function calling
#    (e.g., gemini-1.5-flash-preview-0514, check availability)
response = client.models.generate_content(
  model="gemini-1.5-flash-preview-0514", # <-- Use a valid Vertex model name
  contents=[user_content], # Pass content as a list
  config=genai_types.GenerateContentConfig(
    tools=[
      genai_types.Tool(function_declarations=[get_current_weather_func])]
  )
)

# 5. Print the response (will likely contain a function call)
print(response)

# --- Next Steps (How to handle the response) ---
# Check if the model decided to call the function
if response.candidates[0].content.parts[0].function_call:
    function_call = response.candidates[0].content.parts[0].function_call
    print("\nFunction Call:")
    print(f"  Name: {function_call.name}")
    print(f"  Args: {function_call.args}")

    # Here you would actually call your real weather function
    # e.g., weather_data = get_actual_weather(location=function_call.args['location'])
    # For demonstration, we'll just create dummy data:
    if function_call.name == "get_current_weather" and function_call.args.get('location'):
        location = function_call.args['location']
        api_response_text = f"The weather in {location} is 70 degrees Fahrenheit and sunny."

        # Send the function response back to the model
        function_response_content = genai_types.Content(
            role="function", # Use 'function' role for the response
            parts=[
                genai_types.FunctionResponse(
                    name=function_call.name,
                    response={"weather": api_response_text} # Structure the response as expected
                )
            ]
        )

        print("\nSending Function Response back to model...")

        # Append user message, original model response (function call), and function response
        conversation_history = [
            user_content,
            response.candidates[0].content, # The model's FunctionCall response part
            function_response_content
        ]

        response2 = client.generative_models.generate_content(
            model_name="gemini-1.5-flash-preview-0514",
            contents=conversation_history,
            generation_config=genai_types.GenerationConfig(
                tools=[genai_types.Tool(function_declarations=[get_current_weather_func])]
            )
        )

        print("\nFinal Model Response:")
        print(response2.text)

else:
    print("\nModel did not call the function. Response text:")
    print(response.text)