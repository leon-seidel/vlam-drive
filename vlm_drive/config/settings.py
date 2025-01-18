from pydantic_settings import BaseSettings

class VLMDriveSettings(BaseSettings):
    # VLAM model settings
    vlam_backend: str = "google"                        # VLAM backend, either google or vllm
    vlam_temperature: float = 0.0                       # LLM temperature
    google_api_key: str = ""                            # Only for google backend
    google_model_name: str = "gemini-2.0-flash-exp"     # Only for google backend
    vllm_base_url: str = "http://localhost:8000/v1"     # Only for vllm backend
    vllm_api_key: str = "empty"                         # Only for vllm backend, usually not needed

    # Image settings
    save_images: bool = False
    show_images: bool = True

    # Waypoint settings (change only for custom maps)
    waypoint_file: str = "mine_waypoints.yaml"
    start_waypoint: str = "start"
    first_goal_waypoint: str = "first_sign"

    # Simulation settings (change only for custom installations)
    carla_host: str = "localhost"
    carla_port: int = 2000
    carla_world_name: str = "/Game/Carla/Maps/Mine_01"
    vehicle_bp: str = 'vehicle.miningtruck.miningtruck'
    vehicle_target_speed: float = 15.0
    camera_x: float = 5.5
    camera_z: float = 3.0
    camera_pitch: float = 0.0

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = VLMDriveSettings()