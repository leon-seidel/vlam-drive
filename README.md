# VLAM-based navigation for mining vehicles in Carla UE5.5 simulator
![Demo Image](/media/carla_sim_mine.png)
Demo of using Vision Language Action Models for autonomous navigation between waypoints using simple road signs. The user can give an instruction in natural language like:
```
"Drive the vehicle to Mine B."
```
The VLAM receives an onboard image at each waypoint and decides the direction to drive, determines if the destination has been reached and provides its reasoning. A waypoint handler translates this information into the next waypoint for a Carla agent, where the VLAM kicks in again. 

## Demo run
![Demo Image](/media/mine_B-1.PNG)
![Demo Image](/media/mine_B-2.PNG)
![Demo Image](/media/mine_B-3.PNG)
![Demo Image](/media/mine_B-4.PNG)

## Models
This package can be used either with a cloud VLM via the Google AI API or a locally hosted model using a vLLM OpenAI endpoint. It implements structured JSON outputs for both backends to ensure correctly formatted responses. Tests with Google's `gemini-2.0-flash-exp` show very reliable results, while smaller VLMs like `Pixtral-12B` from Mistral AI worked most of the time. 

## Installation
All tests have been done with Carla UE5.5 0.10.0 using Ubuntu 22.04 and Nvidia GPUs. Because the road signs are added to the simulator, Carla has to be built from source with Unreal Editor. Follow the steps described [here](https://carla-ue5.readthedocs.io/en/latest/build_linux_ue5/) to build Carla UE5.5 on a Linux machine. Then add the signs from `carla/objects/` to the Mine01 simulation environment in Unreal Editor. The Carla UE5.5 build should also install the `carla` Python package in the same version. Check if everything is working and continue with installing this package: 

```bash
git clone https://github.com/leon-seidel/vlam-drive.git
cd vlam-drive
pip install -e .
```
## Configuration
First choose whether to use the Google AI API or a self-hosted vLLM model as a backend. In case of the Google API, the `GOOGLE_API_KEY` has to be acquired from [here](https://aistudio.google.com/app/apikey). You can also choose one of the available Google models in `GOOGLE_MODEL_NAME` while all testing has been done with `gemini-2.0-flash-exp`. 

When using vLLM, the `VLLM_BASE_URL` might have to be configured when running on another machine or port. Running Mistral AI's `Pixtral-12B` has been tested and works with the given setup. This FP8-quantized version of Pixtral runs on a single RTX 3090:
```bash
vllm serve neuralmagic/pixtral-12b-FP8-dynamic --max-model-len 16384
```

All settings for this package can be edited in a `.env` file or using environment variables:

```bash
# Vision Language Model Settings
VLAM_BACKEND=google                       # Options: google, vllm
GOOGLE_API_KEY=your_key_here              # Get from https://aistudio.google.com/app/apikey
GOOGLE_MODEL_NAME=gemini-2.0-flash-exp    # Google Gemini model version
VLLM_BASE_URL=http://localhost:8000/v1    # URL for local VLLM deployment

# Image Settings
SAVE_IMAGES=false                         # Save images with VLAM results
SHOW_IMAGES=true                          # Show images with VLAM results
```

## Running
Start Carla UE5.5 with:
```bash
./CarlaUnreal.sh
```

You can then run the VLM drive navigation with a custom instruction in natural language referring to the 3 available destinations `Mine A`, `Mine B` and `Mine C`:

```bash
python run_vlam_drive.py --instruction "Please drive the vehicle to Mine A."
```
Happy driving!

[Demo Video](https://youtu.be/LhLbKN_zQRg?feature=shared)