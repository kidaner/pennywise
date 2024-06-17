import instructor
from pydantic import Field
import pydantic
from typing import List
from openai import OpenAI
from config import OPENAI_API_KEY

openai_client = instructor.patch(OpenAI(api_key=OPENAI_API_KEY))

class GroItems(pydantic.BaseModel):
    grocery_list: List[str] = Field(..., description=f"List of grocery list items with their quantity descriptions")

def structured_items(grocery_list):
    grocery_items = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_model=GroItems,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that extracts a list of grocery list items and size from a piece of text."},
            {"role": "user", "content": f"Please list the grocery items and their quantity description from this text {grocery_list}"},
        ]
    )

    print(grocery_items.grocery_list)
    
    return list(set(grocery_items.grocery_list))