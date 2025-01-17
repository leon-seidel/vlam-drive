from google import genai
from google.genai import types
from PIL import Image
from os import environ

class GoogleAPI:
    def __init__(self, model_name='gemini-2.0-flash-exp', temperature=0.5):
        # Setup VLM API
        api_key = environ["GOOGLE_API_KEY"]
        self.model_name = model_name
        self.temperature = temperature

        self.client = genai.Client(api_key=api_key)

    def generate_structured_response_from_pil_image(self, full_prompt: str, pil_image: Image.Image, response_schema):
        config = types.GenerateContentConfig(temperature=self.temperature, response_mime_type="application/json",
                                             response_schema=response_schema)

        response = self.client.models.generate_content(model=self.model_name, 
                                                        contents=[pil_image, full_prompt], config=config)

        return response.text
