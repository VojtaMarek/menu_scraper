from dataclasses import dataclass
from typing import Optional, List, Final

from openai import OpenAI
import json
from pydantic import BaseModel

import config

image_description: Final[list] = [
    ("Daal Tadka", 2,
     "Luštěninová kaše – Tadka je indické označení pro koření osmažené na oleji. Obvykle obsahuje římský kmín, "
     "černé hořčičné semínko a chilli papričky."),
    ("Chicken Vindaloo", 4,
     "Kuřecí Vindaloo - pikantní indické jídlo kombinuje kuře s kořením jako je zázvor, česnek a ocet, "
     "které dodávají výraznou a ohnivou chuť."),
    ("Potatoes with green beans", 1,
     "Brambory se zelenými fazolkami - jednoduché, ale výživné jídlo, které spojuje jemnou chuť brambor "
     "a svěží křupavost zelených fazolek."),
    ("Naan, basmati rice, salad, carrots, mango chutney", 1,
     "Naan, basmati rýže, salát, mrkvové, mangový chutney - klasická příloha k indickému jídlu, kde se měkký naan, "
     "nadýchaná basmati rýže a svěží salát doplňují sladko-kyselým mangovým chutney."),
    ("Biryani rice", 0,
     "Biryani rýže - aromatická rýže smíchaná s kořením jako je kardamom, hřebíček a šafrán, "
     "dává tomuto pokrmu bohatou a hlubokou chuť."),
    ("Pudding", 0, "Pudink - jemný a krémový dezert, který je perfektním zakončením bohaté indické hostiny.")
]


# Initialize OpenAI API
client = OpenAI(api_key=config.OPEN_AI_KEY)


# Define the MenuItem dataclass
@dataclass
class MenuItem:
    food_name: str
    spiciness: int
    czech_translation: str


# Define the Menu model using BaseModel from pydantic
class Menu(BaseModel):
    date: Optional[str] = None
    menu: Optional[List[MenuItem]] = None


def process_food_image(pic_url):
    prompt = f"""
    From the provided image url, I need a structured list of food items with their spiciness (on a scale of 0-5 stars) 
    and the Czech translation with a nice short explanation. In case the food is not spicy, please use 0 stars.
    
    Here is an example of the expected output: {image_description} (notice the first item is the food name in English, 
    as shown in the image.)
    
    Date in iso format will be today if it matches the current date, otherwise it will be the date of the image,
    e.g. "01-31-2000". Be carfule about swaping 1 and 7, if not clear use the current date.
    """

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": pic_url}}
        ]}
    ]

    # Call OpenAI GPT API to parse the image description and extract details
    response = client.beta.chat.completions.parse(
        model='gpt-4o-2024-08-06',
        messages=messages,
        response_format=Menu
    )

    # Extract the content
    result = response.choices[0].message.content

    # Try to parse the result into a Python object
    try:
        # Convert the extracted list into a Python object
        food_data = json.loads(result)
        return food_data
    except json.JSONDecodeError:
        return result  # Return raw result if parsing fails


if __name__ == "__main__":
    # Define the image URL
    image_url = ''

    # Process the image and get the structured food data
    food_list = process_food_image(image_url)

    # Output the result
    print(food_list)
