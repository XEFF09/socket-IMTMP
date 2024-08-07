import os
import PIL.Image
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
google_api = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=google_api)

def imageGet(img_path):
    img = PIL.Image.open(f'{img_path}')
    return img

def imageDesc(img_path):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    img = imageGet(img_path)
    text = 'make meme quote from image, no string characters included'

    response = model.generate_content([f"{text}", img])
    return (response.text)