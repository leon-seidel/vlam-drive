import gradio as gr
import time
from typing import Generator
from vlm_drive.simulation.carla_sim import CarlaSim
from vlm_drive.simulation.vehicle import Vehicle
from vlm_drive.simulation.waypoint_handler import WaypointHandler
from vlm_drive.model.vlam import VisionLanguageActionModel



# Simulated backend response generator
def simulate_waypoint_updates(backend: str, instruction: str) -> Generator[tuple, None, None]:
    carla_sim = CarlaSim()
    wp_handler = WaypointHandler()
    vehicle = Vehicle(carla_sim, wp_handler)
    vlam = VisionLanguageActionModel(backend=backend, temperature=0.0)

    print("\nStarting navigation")
    while True:        
        # Drive to destination and take an image
        vehicle.drive_to_next_waypoint()
        destination_image = vehicle.get_current_frame()
        # display(destination_image)
        
        destination_reached, direction_decision, reasoning = vlam.consult(destination_image, instruction)
        yield f"{destination_reached}\n{direction_decision}\n{reasoning}", destination_image

        if not destination_reached:
            wp_handler.update_next_wp_from_direction(direction_decision)
        else:
            print("Destination reached!")
            break

    time.sleep(10)
    vehicle.destroy()

def process_updates(backend: str, instruction: str):
    return simulate_waypoint_updates(backend, instruction).__next__()

# Create the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Vehicle Waypoint Tracker")
    
    with gr.Row():
        # Backend selection dropdown
        backend = gr.Dropdown(
            choices=["google", "vllm"],
            label="Select Backend",
            value="google"
        )
        
        # Instruction input
        instruction = gr.Textbox(label="Enter Instruction", value="Please drive this vehicle to Mine A.")
    
    # Start button
    start_btn = gr.Button("Start Tracking")
    
    # Output displays
    with gr.Row():
        text_output = gr.Textbox(label="Status")
        image_output = gr.Image(label="Waypoint View")
    
    # Connect the components
    start_btn.click(
        fn=process_updates,
        inputs=[backend, instruction],
        outputs=[text_output, image_output],
        api_name="update_stream"
    )

# Launch the interface
if __name__ == "__main__":
    demo.queue().launch()