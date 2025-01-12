from openai import OpenAI
import os 
from dotenv import load_dotenv
import requests
import json

load_dotenv(override=True)

print("OpenAI API Key present:", bool(os.getenv("OPENAI_API_KEY")))
print("OpenWeather API Key present:", bool(os.getenv("OPENWEATHER_API_KEY")))

def get_weather(location: str) -> str:
    """Actually fetch weather data from OpenWeather API"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"  # for Celsius
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"]
        }
    else:
        return {"error": "Failed to get weather data"}

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a specific city",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name to get weather for"
                    }
                },
                "required": ["location"],
                "additionalProperties": False
            }
        }
    }
]

messages = [
    {
        "role": "user",
        "content": "What's the weather like in Paris?"
    }
]

# First call to get the tool call
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools
)

# Handle the tool call
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    
    # Parse the arguments
    args = json.loads(tool_call.function.arguments)
    
    # Call the weather function
    weather_data = get_weather(args["location"])
    
    # Add the assistant's response and tool result to messages
    messages.append(response.choices[0].message)
    messages.append({
        "role": "tool",
        "content": json.dumps(weather_data),
        "tool_call_id": tool_call.id
    })
    
    # Get final response from the model
    final_response = client.chat.completions.create(
        model="gpt-4",
        messages=messages
    )
    
    print(final_response.choices[0].message.content)
else:
    print(response.choices[0].message.content)
