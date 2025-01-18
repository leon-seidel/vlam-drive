import json
from vlm_drive.integrations.google_api import GoogleAPI
from vlm_drive.integrations.vllm_api import VLLMAPI
from vlm_drive.model.templates import NavDescription, navigation_prompt
from vlm_drive.model.utils import add_text_overlay_to_image
from vlm_drive.config import settings
from PIL import Image

class VisionLanguageActionModel:
    def __init__(self):
        backend = settings.vlam_backend
        if backend == "google":
            self.vlm = GoogleAPI()
        elif backend == "vllm":
            self.vlm = VLLMAPI()
        else:
            raise NotImplementedError(f"Backend {backend} not implemented")

    def consult(self, situation_image: Image.Image, instruction: str) -> tuple[bool, str, str]:
        response_schema = NavDescription
        # Fill in the instruction in the prompt
        filled_prompt = navigation_prompt.format(instruction=instruction)
                        
        # Generate structured response from image and convert to dict
        print("VLAM thinking...")
        answer = self.vlm.generate_structured_response_from_pil_image(full_prompt=filled_prompt, 
                                                                      pil_image=situation_image, 
                                                                      response_schema=response_schema)
        answer_dict = json.loads(answer)
        print(f"VLAM output:", answer_dict, "\n")
        
        destination_reached = answer_dict["destination_reached"]
        direction = answer_dict["direction"]
        reasoning = answer_dict["reasoning"]
        
        # If requested to show or save images add text overlay
        if settings.show_images or settings.save_images:
            add_text_overlay_to_image(situation_image, instruction, destination_reached, direction, reasoning)
        
        return destination_reached, direction, reasoning
    
    
