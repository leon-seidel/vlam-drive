import carla

class CarlaSim:
    def __init__(self, world_name="/Game/Carla/Maps/Mine_01"):
        # Connect to the client and retrieve the world object
        self.client = carla.Client('localhost', 2000)
        self.world = self.client.get_world()
        self.client.load_world(world_name)

        # Create map and traffic manager
        self.map = self.world.get_map()
        self.traffic_manager = self.client.get_trafficmanager(8000)
        self.tm_port = self.traffic_manager.get_port()

        # Get the blueprint library
        self.blueprint_library = self.world.get_blueprint_library()
