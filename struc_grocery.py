from gro_zip import grocery_city
import instructor
from pydantic import Field
import pydantic
from typing import List
from openai import OpenAI
from config import OPENAI_API_KEY

openai_client = instructor.patch(OpenAI(api_key=OPENAI_API_KEY))

class GroInfo(pydantic.BaseModel):
    "Correctly extracted grocery store names"
    groceries: List[str] = Field(..., description=f"List of grocery stores")

def structured_grocery(city):
    grocery_store = openai_client.chat.completions.create(
    model="gpt-3.5-turbo",
    response_model=GroInfo,
    messages=[
        {"role": "system", "content": "You are a helpful assistant that extracts a list of grocery store names."},
        {"role": "user", "content": f"Please list the grocery store names from {grocery_city(city)}"},
    ]
    )

    return grocery_store.groceries