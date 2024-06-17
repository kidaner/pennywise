import requests
import pandas as pd
from pydantic import BaseModel, Field
import instructor
from openai import OpenAI
import time
import json
from config import PERPLEXITY_API_KEY, OPENAI_API_KEY

openai_client = instructor.patch(OpenAI(api_key=OPENAI_API_KEY))

class PriceInfo(BaseModel):
    price: float = Field(..., description="Price of the item at the store")

rate_limit_counter = 0

def fetch_grocery_price(item, store, city):
    global rate_limit_counter

    if rate_limit_counter >= 19:
        print("Rate limit reached. Waiting for a minute...")
        time.sleep(60)
        rate_limit_counter = 0
    
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
                "content": f"What is the price of {item} at {store} in {city}?"
            }
        ]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        rate_limit_counter += 1
    except requests.exceptions.RequestException as e:
        print(f"Error fetching price for {item} at {store} in {city}: {e}")
        return None

    try:
        response_dict = response.json()
        content = response_dict['choices'][0]['message']['content']
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing response for {item} at {store} in {city}: {e}")
        return None

    try:
        price_info = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            response_model=PriceInfo,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts the price of a grocery item."},
                {"role": "user", "content": f"Get the price of {content}"},
            ]
        )
        return price_info.price
    
    except Exception as e:
        print(f"Error processing OpenAI response for {item} at {store} in {city}: {e}")
        return None

def create_grocery_price_matrix(items, stores, city):
    price_matrix = pd.DataFrame(index=items, columns=stores)
    
    for item in items:
        for store in stores:
            price = fetch_grocery_price(item, store, city)
            price_matrix.loc[item, store] = price
    
    price_matrix_filled = price_matrix.fillna(0)
    price_matrix_filled.loc['Total'] = price_matrix_filled.sum()
    
    return price_matrix_filled