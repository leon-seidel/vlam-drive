from google import genai
from google.genai import types
from PIL import Image
from vlm_drive.config import settings

class GoogleAPI:
    def __init__(self):
        # Setup VLM API
        self.model_name = settings.google_model_name
        self.temperature = settings.vlam_temperature
        
        self.client = genai.Client(api_key=settings.google_api_key)
        print(f"Connected to {self.model_name}")

    def generate_structured_response_from_pil_image(self, full_prompt: str, pil_image: Image.Image, 
                                                    response_schema: type) -> str:
        config = types.GenerateContentConfig(temperature=self.temperature, response_mime_type="application/json",
                                             response_schema=response_schema)

        response = self.client.models.generate_content(model=self.model_name, 
                                                        contents=[pil_image, full_prompt], config=config)

        return response.text
