import queue
import numpy as np
from PIL import Image
from carla import VehicleControl, Location, Rotation, Transform
from vlm_drive.config import settings
from vlm_drive.simulation.agents.navigation.basic_agent import BasicAgent

class Vehicle:
    def __init__(self, carla_sim, waypoint_handler):
        # Initialize vehicle
        self.wp_handler = waypoint_handler
        self.world, self.map, self.blueprint_library = carla_sim.world, carla_sim.map, carla_sim.blueprint_library
        self.image_queue = queue.Queue(1)
        self.ego_vehicle, self.camera, self.agent = self.create_vehicle(settings.vehicle_bp, settings.vehicle_target_speed)

    def create_vehicle(self, vehicle_bp, target_speed):
        # Spawn vehicle
        spawn_waypoint = self.wp_handler.get_spawn_waypoint()
        ego_bp = self.blueprint_library.find(vehicle_bp)
        ego_bp.set_attribute('role_name', 'hero')
        ego_vehicle = self.world.spawn_actor(ego_bp, spawn_waypoint)
        # Init with brake
        ego_vehicle.apply_control(VehicleControl(brake=1.0, hand_brake=True))

        # Add camera
        camera_init_trans = Transform(Location(x=settings.camera_x, z=settings.camera_z),
                                      Rotation(pitch=settings.camera_pitch))
        camera_bp = self.blueprint_library.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x', '1280')
        camera_bp.set_attribute('image_size_y', '720')
        camera = self.world.spawn_actor(camera_bp, camera_init_trans, attach_to=ego_vehicle)
        camera.listen(self.process_image)

        # Setup agent
        agent = BasicAgent(ego_vehicle, map_inst=self.map, target_speed=target_speed)

        return ego_vehicle, camera, agent

    def drive_to_next_waypoint(self):
        # Get next waypoint and drive there
        next_wp_location = self.wp_handler.get_next_waypoint().location
        self.drive_to_location(next_wp_location)

    def drive_to_location(self, location):
        # Refine location with the map and set it as destination
        refined_location = self.map.get_waypoint(location).transform.location
        self.agent.set_destination(refined_location)

        # Release brake and hand brake
        self.ego_vehicle.apply_control(VehicleControl(brake=0.0, hand_brake=False))
        
        # Drive until location is reached
        print("\nDriving...")
        while True:
            if self.agent.done():
                # Set brake and handbrake
                self.ego_vehicle.apply_control(VehicleControl(brake=1.0, hand_brake=True))
                # Update current waypoint
                self.wp_handler.update_current_waypoint()
                print("Location has been reached.")
                break

            self.ego_vehicle.apply_control(self.agent.run_step())

    def process_image(self, image):
        # image.save_to_disk('./images/%.6d.jpg' % image.frame)
        if not self.image_queue.empty():
            self.image_queue.get()
        self.image_queue.put(image)

    def get_current_frame(self) -> Image.Image:
        carla_image = self.image_queue.get()
        image_data = np.frombuffer(carla_image.raw_data, dtype=np.uint8).reshape((carla_image.height, carla_image.width, 4))[:, :, [2, 1, 0, 3]].astype('uint8')
        return Image.fromarray(image_data)
    
    def destroy(self):
        self.ego_vehicle.destroy()
        self.camera.destroy()
