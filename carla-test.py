import carla
import math
import random
import time
import queue
import numpy as np
import cv2

client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world  = client.get_world()
bp_lib = world.get_blueprint_library()

# Get the map spawn points
spawn_points = world.get_map().get_spawn_points()

# spawn vehicle
vehicle_blueprints = world.get_blueprint_library().filter('*vehicle*')
vehicle = world.try_spawn_actor(random.choice(vehicle_blueprints), random.choice(spawn_points))

# spawn camera
camera_bp = bp_lib.find('sensor.camera.rgb')
camera_init_trans = carla.Transform(carla.Location(z=2))
camera = world.spawn_actor(camera_bp, camera_init_trans, attach_to=vehicle)
# vehicle.set_autopilot(True)

# Set up the simulator in synchronous mode
settings = world.get_settings()
settings.synchronous_mode = True # Enables synchronous mode
settings.fixed_delta_seconds = 0.05
world.apply_settings(settings)

# Create a queue to store and retrieve the sensor data
image_queue = queue.Queue()
camera.listen(image_queue.put)


while True:
    world.tick()
    image = image_queue.get()

    # Reshape the raw data into an RGB array
    img = np.reshape(np.copy(image.raw_data), (image.height, image.width, 4)) 

    # Display the image in an OpenCV display window
    cv2.namedWindow('ImageWindowName', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('ImageWindowName',img)
    cv2.waitKey(1)