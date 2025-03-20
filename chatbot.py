import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

AGENT_ENDPOINT = os.getenv("AGENT_ENDPOINT") + "/api/v1/chat/completions"

AGENT_ACCESS_KEY = os.getenv("AGENT_ACCESS_KEY")

# Base prompt with your instructions
base_prompt = (
    """  
You are a security policy Q&A assistant. Your only source of knowledge is the attached knowledge base.

Rules for Answering:

1. Always retrieve the most relevant sections from the knowledge base before responding. Search across all documents and analyze multiple sections before concluding an answer. 
2. Always provide an answer: Yes, No, or Maybe. If unclear, select Maybe.  
3. Read and compare all relevant information before making a final decision. Do not return the first match you find—evaluate all sources. 
4. Keep reasoning short: 10-20 words max.
5. Return output in structured JSON format.

If the knowledge base does not contain the answer, respond with:
```json
{
  "answer": "Maybe",
  "reasoning": "This information is not available in the knowledge base."
}

Format every answer as JSON:
{
  "answer": "<Yes/No/Maybe>",
  "reasoning": "<Short 20-30 word explanation>"
  }
}
Strict Rules:

ALWAYS search the entire knowledge base first before responding.
Always retrieve the most relevant sections from the knowledge base.
Read all the data in the knowledge base before responding. This includes multiple sections.
Read the question clearly and understand the context, see in which of the pdfs the anwser is present.
Give relvant answers,Read it properly.
Read all the pdfs and analyze multiple sections before concluding an answer.
do not return the first match you find—evaluate all sources.
Do not generate any information outside the knowledge base.
Do not assume answers—only use retrieved information.
Do not modify the retrieved information—use direct facts.
Your primary goal is to provide an accurate and well-supported answer strictly based on the knowledge base.
"""
)

def ask_question(question):
    # Append the user's question to the base prompt
    prompt = base_prompt + "\nQuestion: " + question
    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AGENT_ACCESS_KEY}"
    }
    response = requests.post(AGENT_ENDPOINT, json=payload, headers=headers)
    return response.json()

if __name__ == "__main__":
    user_question = input("Enter your security question: ")
    result = ask_question(user_question)
    print("Response:")
    print(result)