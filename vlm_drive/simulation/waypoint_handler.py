from carla import Location, Rotation, Transform

class WaypointHandler:
    def __init__(self, start_waypoint="start", first_goal_waypoint="first_sign"):
        self.waypoints = {
            "start": Transform(Location(x=-300.2, y=-287.8, z=82.5), Rotation(yaw=0)),
            "first_sign": Transform(Location(x=-140, y=-224, z=76), Rotation(yaw=25)),
            "mid3": Transform(Location(x=185.6, y=-15.3, z=-24), Rotation(yaw=35)),
            "first_left_goal": Transform(Location(x=237.9, y=-267.5, z=80), Rotation(yaw=90)),
            "mid1": Transform(Location(x=-60.4, y=260.8, z=36), Rotation(yaw=180)),
            "mid2": Transform(Location(x=70, y=-69, z=-15), Rotation(yaw=40)),
            "second_sign": Transform(Location(x=163, y=-31.4, z=-20), Rotation(yaw=40)),
            "second_straight_goal": Transform(Location(x=51, y=181, z=-39), Rotation(yaw=180)),
            "second_right_goal": Transform(Location(x=46, y=74, z=-57), Rotation(yaw=180)),
        }

        self.spawn_waypoint = start_waypoint
        self.current_waypoint = start_waypoint
        self.next_waypoint = first_goal_waypoint

    def get_spawn_waypoint(self):
        return self.waypoints[self.spawn_waypoint]
    
    def get_current_waypoint(self):
        return self.waypoints[self.current_waypoint]
    
    def get_next_waypoint(self):
        return self.waypoints[self.next_waypoint]

    def update_current_waypoint(self):
        self.current_waypoint = self.next_waypoint

    def update_next_wp_from_direction(self, direction_decision: str):
        if self.current_waypoint == "first_sign":
            if direction_decision == "left":
                self.next_waypoint = "first_left_goal"
            elif direction_decision == "straight":
                self.next_waypoint = "second_sign"
        elif self.current_waypoint == "second_sign":
            if direction_decision == "straight":
                self.next_waypoint = "second_straight_goal"
            elif direction_decision == "right":
                self.next_waypoint = "second_right_goal"
        else:
            print("No waypoint found for direction decision")
