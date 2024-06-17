import requests
from config import PERPLEXITY_API_KEY
import json

def grocery_city(city):

    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
        'Authorization': f'Bearer {PERPLEXITY_API_KEY}'
    }

    payload = {
        "model": "sonar-small-online",
        "stream": False,
        "max_tokens": 300,
        "frequency_penalty": 1,
        "temperature": 0.0,
        "messages": [
            {
                "role": "system",
                "content": "Be precise and concise in your responses."
            },
            {
                "role": "user",
                "content": f"List 3 largest groceries in {city}"
            }
        ]
    }

    payload["streaming_finished"] = True

    response = requests.post(url, json=payload, headers=headers)
    response_dict = json.loads(response.text)
    return response_dict['choices'][0]['message']['content']