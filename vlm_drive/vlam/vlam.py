import json
from vlm_drive.integrations.google_api import GoogleAPI
from vlm_drive.integrations.vllm_api import VLLMAPI
from vlm_drive.vlam.templates import NavDescription, navigation_prompt

class VisionLanguageActionModel:
    def __init__(self, backend="google", temperature=0.0):
        if backend == "google":
            self.vlm = GoogleAPI(temperature=temperature)
        elif backend == "vllm":
            self.vlm = VLLMAPI(temperature=temperature)
        else:
            raise NotImplementedError(f"Backend {backend} is not implemented.")

    def consult(self, destination_image, instruction):
        response_schema = NavDescription
        filled_prompt = navigation_prompt.format(instruction=instruction)

        answer = self.vlm.generate_structured_response_from_pil_image(filled_prompt, destination_image, response_schema=response_schema)
        answer_dict = json.loads(answer)
        print(answer_dict)
        return answer_dict["goal_reached"], answer_dict["direction"]
