import carla
from vlm_drive.config import settings

class CarlaSim:
    def __init__(self):
        # Connect to the client and retrieve the world object
        self.client = carla.Client(settings.carla_host, settings.carla_port)
        self.client.load_world(settings.carla_world_name)
        self.world = self.client.get_world()

        # Create map
        self.map = self.world.get_map()

        # Get the blueprint library
        self.blueprint_library = self.world.get_blueprint_library()
