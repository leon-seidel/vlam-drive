from openai import OpenAI
import time
from PIL import Image
import base64
from io import BytesIO
from os import environ

class VLLMAPI:
    def __init__(self, api_url="http://localhost:8000/v1", temperature=0.5):
        # Setup VLM API
        api_key = str(environ.get("VLLM_API_KEY"))      # Usually not needed
        self.temperature = temperature
        self.connection_timeout = 5  # Time to wait before trying to connect again
        self.vlm_client, self.model_name = self.connect_to_vlm(api_url, api_key)

    def connect_to_vlm(self, api_url, api_key):
        while True:
            try:
                vlm_client = OpenAI(api_key=api_key, base_url=api_url)
                models = vlm_client.models.list()
                model_name = models.data[0].id
                print(f"Connected to {model_name}")
                return vlm_client, model_name
            except Exception as e:
                print("No model on this API yet...", e)
                time.sleep(self.connection_timeout)
                continue   
    
    def generate_structured_response_from_pil_image(self, full_prompt: str, pil_image: Image.Image, response_schema):
        chat_completion_from_base64 = self.vlm_client.chat.completions.create(
            messages=self.create_vlm_messages(full_prompt, pil_image),
            model=self.model_name,
            temperature=self.temperature,
            extra_body={
                "guided_json": response_schema.model_json_schema()
            }
        )
        return chat_completion_from_base64.choices[0].message.content

    def create_vlm_messages(self, full_prompt: str, pil_image: Image.Image):
        image_url = f"data:image/jpeg;base64,{self.pil_image_to_base64(pil_image)}"
        messages=[
                    {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": full_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                                },
                        },
                        ]
                    }
                ]
        return messages
    
    def pil_image_to_base64(self, pil_image):
        buffered = BytesIO()
        pil_image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
