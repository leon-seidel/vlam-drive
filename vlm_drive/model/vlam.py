import json
from vlm_drive.integrations.google_api import GoogleAPI
from vlm_drive.integrations.vllm_api import VLLMAPI
from vlm_drive.model.templates import NavDescription, navigation_prompt

class VisionLanguageActionModel:
    def __init__(self, backend="google", temperature=0.0):
        if backend == "google":
            self.vlm = GoogleAPI(temperature=temperature)
        elif backend == "vllm":
            self.vlm = VLLMAPI(temperature=temperature)
        else:
            raise NotImplementedError(f"Backend {backend} not implemented")

    def consult(self, destination_image, instruction):
        response_schema = NavDescription
        # Fill in the instruction in the prompt
        filled_prompt = navigation_prompt.format(instruction=instruction)
                        
        # Generate structured response from image and convert to dict
        print("VLAM thinking...")
        answer = self.vlm.generate_structured_response_from_pil_image(full_prompt=filled_prompt, 
                                                                      pil_image=destination_image, 
                                                                      response_schema=response_schema)
        answer_dict = json.loads(answer)
        print(f"VLAM output:", answer_dict, "\n")
        
        return answer_dict["destination_reached"], answer_dict["direction"], answer_dict["reasononing"]
