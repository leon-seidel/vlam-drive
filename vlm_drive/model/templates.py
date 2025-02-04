from pydantic import BaseModel

class NavDescription(BaseModel):
            reasoning: str
            direction: str
            destination_reached: bool

navigation_prompt = """
You are navigating a mining vehicle, and are given the following instruction as navigation destination goal:
{instruction}

There are three Mines A, B and C and there are different road signs leading towards them. Keep goings straight if there is no sign for 
the instructed destination. The mines itself have a sign without a direction.
At every sign you are prompted to give a direction out of "right", "left" and "straight", a short reasoning for your decision
in the following JSON schema and wheter you reached the given destination:

{{"reasoning": brief sentence, "direction": "right OR left OR straight", "destination_reached": true/false}}

Start with the reasoning to come to a conclusion before deciding on the direction.
"""
