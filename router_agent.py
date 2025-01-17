from openai import OpenAI
import os 
from dotenv import load_dotenv
import requests
import json

load_dotenv(override=True)

def router_agent(prompt: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """You are a LLM router agent. Your job is to route user input to the correct model based on the following criteria:

1. If the user input requires extensive reasoning to answer, route to the reasoning_agent
2. If the request involves math or coding problems, route to the reasoning_agent
3. If the request only needs a simple conversational answer, route to the conversational_agent

Please respond with only the name of the appropriate agent."""},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content

def reasoning_agent(prompt: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a reasoning agent. You are tasked with solving complex problems that require extensive reasoning, including math and coding problems."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content

def conversational_agent(prompt: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a conversational agent. You are tasked with engaging in friendly dialogue and providing simple, direct answers to conversational questions."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content

def process_request(prompt: str) -> str:
    # Get the routing decision
    route_to = router_agent(prompt).lower().strip()
    
    # Route to the appropriate agent
    if "reasoning" in route_to:
        return reasoning_agent(prompt)
    elif "conversational" in route_to:
        return conversational_agent(prompt)
    else:
        return "Error: Unable to determine appropriate agent for this request."

if __name__ == "__main__":
    while True:
        user_input = input("\nEnter your question (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        response = process_request(user_input)
        print("\nResponse:", response)