from mistralai import Mistral
import json

def create_mistral_agent(api_key = "qIzgJeXyROO9gZ6AIHWsgQKCYh5jgOCd"):
    return Mistral(api_key=api_key)

def answer_check(answer, question):
    client = create_mistral_agent()
    chat_response = client.agents.complete(
    agent_id="ag:edc8f481:20250131:clear-text:ba9a032b",
    messages=[
        {
            "role": "user",
            "content": f"(Считаешь ли ты ответ {answer} на вопрос {str(question)} корректным ",
        },
        
    ],
    )
    return json.dumps({"chunks": chat_response.choices[0].message.content})