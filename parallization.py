from openai import OpenAI
import os
from dotenv import load_dotenv
import asyncio
from typing import Tuple

load_dotenv(override=True)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def technical_evaluator(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a technical evaluator. Analyze the question from a technical perspective, considering accuracy, complexity, and technical feasibility. Focus on mathematical correctness and technical implementation details."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

async def practical_evaluator(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a practical evaluator. Analyze the question from a practical perspective, considering real-world applicability, user experience, and implementation challenges. Focus on usability and practical considerations."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

def synthesizer_agent(responses: Tuple[str, str]) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a synthesis agent. Combine the technical and practical evaluations into a comprehensive final answer. Consider both perspectives equally and provide a balanced recommendation."},
            {"role": "user", "content": f"Technical Evaluation: {responses[0]}\nPractical Evaluation: {responses[1]}\nPlease synthesize a final response that considers both aspects."}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

async def process_parallel(prompt: str):
    # Run parallel evaluations
    evaluations = await asyncio.gather(
        technical_evaluator(prompt),
        practical_evaluator(prompt)
    )
    
    print("\nAnalytical Response:")
    print(evaluations[0])
    print("\nCreative Response:")
    print(evaluations[1])
    
    # Synthesize the evaluations
    final_response = synthesizer_agent(evaluations)
    print("\nFinal Synthesis:")
    print(final_response)
    return final_response

if __name__ == "__main__":
    while True:
        user_input = input("\nEnter your question (or 'quit' to exit): ")
        if user_input.lower() == 'quit':
            break
        asyncio.run(process_parallel(user_input))
