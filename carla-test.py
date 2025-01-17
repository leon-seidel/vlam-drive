from vlm_drive.simulation.carla_sim import CarlaSim
from vlm_drive.simulation.vehicle import Vehicle
from vlm_drive.simulation.waypoint_handler import WaypointHandler
from vlm_drive.model.vlam import VisionLanguageActionModel
import time

carla_sim = CarlaSim()
wp_handler = WaypointHandler(start_waypoint="start", first_goal_waypoint="first_sign")
vehicle = Vehicle(carla_sim, wp_handler)
vlam = VisionLanguageActionModel(backend="google", temperature=0.0)

instruction = "Please drive this vehicle to Mine B."

print("\nStarting navigation")
while True:        
    # Drive to destination and take an image
    vehicle.drive_to_next_waypoint()
    destination_image = vehicle.get_current_frame()
    # display(destination_image)
    
    destination_reached, direction_decision = vlam.consult(destination_image, instruction)

    if not destination_reached:
        wp_handler.update_next_wp_from_direction(direction_decision)
    else:
        print("Destination reached!")
        break

time.sleep(10)
vehicle.destroy()