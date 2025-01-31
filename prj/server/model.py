from mistralai import Mistral
from langchain.agents import initialize_agent, Tool, AgentType
from langchain.agents import AgentExecutor
from langchain.prompts import PromptTemplate
from tools_config import tools

def create_mistral_agent(api_key = "qIzgJeXyROO9gZ6AIHWsgQKCYh5jgOCd"):
    return Mistral(api_key=api_key)

client = create_mistral_agent()

def ai_agent(question: str) -> str:
    chat_response = client.agents.complete(
    agent_id="ag:edc8f481:20250131:ll:48e9f549",
    messages=[
        {
            "role": "user",
            "content": f"ответь на вопрос {str(question)}",
        },
        
    ],
    tools=tools, 
    tool_choice="auto"
)
    return chat_response.choices[0].message.content
