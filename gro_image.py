import requests
import base64
from config import NVIDIA_API_KEY

def extract_grocery_list(uploaded_file):
    invoke_url = "https://ai.api.nvidia.com/v1/vlm/adept/fuyu-8b"

    image_b64 = base64.b64encode(uploaded_file.read()).decode()

    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Accept": "application/json"
    }

    payload = {
        "messages": [
            {
                "role": "user",
                "content": f'List all the grocery items in the image <img src="data:image/jpg;base64,{image_b64}" />'
            }
        ],
        "max_tokens": 1024,
        "temperature": 0.20,
        "top_p": 0.70,
    }

    response = requests.post(invoke_url, headers=headers, json=payload)

    content = response.json()['choices'][0]['message']['content']

    print(content)
    
    return content