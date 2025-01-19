import argparse
from vlm_drive.simulation.vehicle import Vehicle
from vlm_drive.simulation.waypoint_handler import WaypointHandler
from vlm_drive.model.vlam import VisionLanguageActionModel
from vlm_drive.simulation.carla_sim import CarlaSim

def run_vlam_drive(instruction: str):
    carla_sim = CarlaSim()
    wp_handler = WaypointHandler()
    vehicle = Vehicle(carla_sim, wp_handler)
    vlam = VisionLanguageActionModel()

    print("\nStarting...")
    while True:        
        # Get image from vehicle 
        situation_image = vehicle.get_current_frame()
        # Consult VLAM for decision on what to do next
        destination_reached, direction_decision, reasoning = vlam.consult(situation_image, instruction)

        # Update vehicle state based on VLAM decision
        if not destination_reached:
            # Update waypoint and drive to it
            wp_handler.update_next_wp_from_direction(direction_decision)
            vehicle.drive_to_next_waypoint()
        else:
            print("Destination reached!")
            break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-I', '--instruction', type=str)
    args = parser.parse_args()
    # Run VLAM drive navigation
    run_vlam_drive(args.instruction)

if __name__ == "__main__":
    main()
