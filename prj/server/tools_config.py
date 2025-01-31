import functools

from ..tools.answer_check import answer_check


answer_check = {
        "type": "function",
        "function": {
            "name": "answer_check",
            "description": "Функция для проверки полноты ответа.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Актуализированная информация.",
                    }
                },
                "required": ["query"],
            },
        },
}

tools = [ answer_check]