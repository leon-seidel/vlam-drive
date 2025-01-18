import yaml
from importlib.resources import files
from vlm_drive.config import settings
from carla import Location, Rotation, Transform

class WaypointHandler:
    def __init__(self):
        # Open waypoint file
        waypoint_file_path = files("vlm_drive.config").joinpath(settings.waypoint_file)
        with open(waypoint_file_path, 'r') as file:
            self.waypoints = yaml.safe_load(file)["waypoints"]

        # Initialize waypoints
        self.spawn_waypoint = settings.start_waypoint
        self.current_waypoint = settings.start_waypoint
        self.next_waypoint = settings.first_goal_waypoint

    def convert_to_carla_transform(self, wp):
        wp_transform = wp["transform"]
        return Transform(Location(x=wp_transform["x"], y=wp_transform["y"], z=wp_transform["z"]), 
                         Rotation(yaw=wp_transform["yaw"]))

    def get_spawn_waypoint(self):
        wp = self.waypoints[self.spawn_waypoint]
        return self.convert_to_carla_transform(wp)
    
    def get_current_waypoint(self):
        wp = self.waypoints[self.current_waypoint]
        return self.convert_to_carla_transform(wp)
    
    def get_next_waypoint(self):
        wp = self.waypoints[self.next_waypoint]
        return self.convert_to_carla_transform(wp)

    def update_current_waypoint(self):
        self.current_waypoint = self.next_waypoint

    def update_next_wp_from_direction(self, direction_decision: str):
        possible_next_waypoints = self.waypoints[self.current_waypoint]["next_waypoints"]
        if possible_next_waypoints is None or direction_decision not in possible_next_waypoints:
            print("No waypoint found for direction decision")
            return
        self.next_waypoint = possible_next_waypoints[direction_decision]

