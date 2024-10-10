from dotenv import load_dotenv
from pdf2image import convert_from_path
import base64
import requests
import os

load_dotenv()

## get openai api key
api_key = os.getenv("OPENAI_API_KEY")

## encode image
def encode_image(image_path: str) -> str:
    '''
    Encode an image file into a base64 string.
    Args:
        image_path (str): The path to the image file.

    Returns:
        str: The base64 encoded image.
    '''
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def read_image(pdf_path: str, image_quality: int = 60, limit: int = 10) -> str:
    '''
    Read a pdf and turn it into text using OpenAI's API.

    Args:
        pdf_path (str): The path to the pdf file.
        image_quality (int): The quality of the image to convert from the pdf. (greatly affects quality/cost)
        limit (int): The number of pages to process.

    Returns:
        str: The text from the pdf.
    '''
    responses = []

    ## turn pdf into images
    images = convert_from_path(pdf_path, dpi=image_quality)
    for i, image in enumerate(images):
        print(f"Processing page {i + 1}")

        ## limit the number of pages processed
        if limit:
            if i+1 > limit:
                break
        
        image.save(f'page_{i + 1}.png', 'PNG')
        image_path = f"page_{i + 1}.png"

        ## encode image
        base64_image = encode_image(image_path)

        ## call openai
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                        "type": "text",
                        "text": "Turn this image into text. Return the text in JSON format."
                        },
                        {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                        }
                    ]
                }
            ]
        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        responses.append(response.json()["choices"][0]["message"]["content"])

        ## get rid of created images
        os.remove(image_path)

    ## combine responses and clean up the text
    text = '\n'.join(responses)
    clean_text = text.replace('```', '').replace('json', '').strip()
    return clean_text