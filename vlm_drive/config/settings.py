from pydantic_settings import BaseSettings

class VLMDriveSettings(BaseSettings):
    # VLAM model settings
    vlam_backend: str = "google" # google or vllm
    vlam_temperature: float = 0.0
    
    # For vlam_backend="google"
    google_api_key: str = ""
    google_model_name: str = "gemini-2.0-flash-exp"
    
    # For vlam_backend="vllm"
    vllm_api_key: str = "empty"  # Usually not needed
    vllm_base_url: str = "http://localhost:8000/v1"

    # Image settings
    save_images: bool = False
    show_images: bool = True

    # Waypoint settings
    waypoint_file: str = "mine_waypoints.yaml"
    start_waypoint: str = "start"
    first_goal_waypoint: str = "first_sign"

    # Simulation settings
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