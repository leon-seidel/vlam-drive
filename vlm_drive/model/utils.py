import time
import base64
from io import BytesIO
from importlib.resources import files
from PIL import Image, ImageDraw, ImageFont
from vlm_drive.config import settings

def add_text_overlay_to_image(image: Image.Image, instruction: str, destination_reached: bool, 
                              direction: str, reasoning: str) -> Image.Image:
    # Create draw
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except IOError:
        font = ImageFont.load_default()
    
    # Position text in top-left corner with padding
    x, y = 10, 10
    line_height = 25
    
    # Add white text with black outline for readability
    texts = [
        f"Instruction: {instruction}",
        "Answer from VLAM:",
        f"   Reasoning: {reasoning[:200]}..." if len(reasoning) > 200 else f"   Reasoning: {reasoning}",
        f"   Direction: {direction}",
        f"   Destination reached: {destination_reached}"
    ]
    
    for text in texts:
        for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
            draw.text((x+dx, y+dy), text, font=font, fill='white')
        draw.text((x, y), text, font=font, fill='black')
        y += line_height
    
    # Save and show save image if requested
    if settings.save_images:
        image_filename = files("vlm_drive.images").joinpath(f"{time.time()}.png")
        image.save(image_filename)
    if settings.show_images:
        image.show()

def pil_image_to_base64(pil_image: Image.Image) -> str:
    buffered = BytesIO()
    pil_image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')
