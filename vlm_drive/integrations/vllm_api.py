from openai import OpenAI
import time
from PIL import Image
from vlm_drive.config import settings
from vlm_drive.model.utils import pil_image_to_base64

class VLLMAPI:
    def __init__(self):
        # Setup VLM API
        base_url = settings.vllm_base_url
        api_key = settings.vllm_api_key      # Usually not needed
        self.temperature = settings.vlam_temperature
        self.connection_timeout = 5  # Time to wait before trying to connect again
        self.vlm_client, self.model_name = self.connect_to_vlm(base_url, api_key)

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
    
    def generate_structured_response_from_pil_image(self, full_prompt: str, pil_image: Image.Image, 
                                                    response_schema: type) -> str:
        chat_completion_from_base64 = self.vlm_client.chat.completions.create(
            messages=self.create_vlm_messages(full_prompt, pil_image),
            model=self.model_name,
            temperature=self.temperature,
            extra_body={
                "guided_json": response_schema.model_json_schema()
            }
        )
        return chat_completion_from_base64.choices[0].message.content

    def create_vlm_messages(self, full_prompt: str, pil_image: Image.Image) -> list[dict]:
        image_url = f"data:image/jpeg;base64,{pil_image_to_base64(pil_image)}"
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
    