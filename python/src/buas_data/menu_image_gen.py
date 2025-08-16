from __future__ import annotations
import os
import sys
from typing import Dict, Optional
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import argparse
import yaml

# Only import heavy dependencies when needed
def get_diffusion_pipeline():
    try:
        from diffusers import StableDiffusionPipeline
        import torch
        return StableDiffusionPipeline, torch
    except ImportError:
        print("Diffusion dependencies not installed. Run: pip install diffusers torch")
        sys.exit(1)
        import torch
        return StableDiffusionPipeline, torch
    except ImportError:
        print("❌ Diffusion dependencies not installed. Run: pip install diffusers torch torchvision")
        sys.exit(1)

TEMPLATES: Dict[str, str] = {
    "HUMMUS": r"""
        .-~~~~~~~~~~~~~~~~~~~~~~~~-.
      .'   _   _   _   _   _   _    '.
     /    (_) (_) (_) (_) (_) (_)      \
    |   .--------------------------.    |
    |   |      HUMMUS  BOWL        |    |
    |   |  ~~ tahini  ~~  olive ~~ |    |
    |   |  .. beef ..  pine  ...   |    |
    |   '--------------------------'    |
     \        (pomegranate *)           /
      '.     _   _   _   _   _        .'
        '-~~~~~~~~~~~~~~~~~~~~~~~~~~-'
    """,

    "EGGPLANT": r"""
             ___
         .-"`   `"-.
        /  .-'''-.  \
       /  /        \  \
      |  |  MTABBAL | |
      |  |  ~~~~~~~ | |
      |  | tahini   | |
       \  \  cumin /  /
        \  '.___.'  /
         '-._____.-'
    """,

    "BREAD": r"""
      _______________________________
     /                               \
    |     MANAKISH — ZA'ATAR         |
    |  [====  flatbread  ====]       |
    |   blistered • chewy • warm     |
     \_______________________________/
    """,

    "KEBAB": r"""
    grill >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
     |\  |\  |\  |\  |\  |\  |\  |\  |\
     ||\ ||\ ||\ ||\ ||\ ||\ ||\ ||\ ||\
     || \|| \|| \|| \|| \|| \|| \|| \|| \
     ||--(lamb)--(chicken)--(beef)--(kofta)--||
     ||  skewers • parallel • hot cluster    ||
     ||______________________________________||
    """,

    "MEZZE": r"""
     .--------------------------------------.
     |   SURPRISE  MEZZE  (streaming)       |
     |  small bowls • dips • pickles • fun  |
     |  checkpoints to avoid skew & hunger  |
     '--------------------------------------'
    """,

    "SHARE": r"""
     ________   ________   ________
    /  ____  \ /  ____  \ /  ____  \
   |  |____|  |  herbs  | |  olive |  -> replicated across nodes
    \________/  ________/  \___oil_/
    """,
}


FALLBACK = r"""
  [no template]
  This item has no dedicated ASCII template.
  Add one in TEMPLATES using the key listed in dishes.yaml.
"""


def image_to_ascii(image_path: str, width: int = 80, height: int = 40) -> str:
    """Convert an image to ASCII art."""
    try:
        # ASCII characters from darkest to lightest
        ascii_chars = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
        
        # Open and process image
        img = Image.open(image_path)
        
        # Convert to grayscale
        img = img.convert('L')
        
        # Resize image
        img = img.resize((width, height))
        
        # Convert pixels to ASCII
        pixels = img.getdata()
        ascii_str = ""
        
        for i, pixel in enumerate(pixels):
            if i % width == 0 and i != 0:
                ascii_str += "\n"
            
            # Map pixel brightness to ASCII character
            ascii_str += ascii_chars[pixel // 25]  # 255 / 10 ≈ 25
        
        return ascii_str
        
    except Exception as e:
        return f"Error converting image to ASCII: {e}"


def generate_dish_image(item: dict, output_dir: str = "generated_images") -> Optional[str]:
    """Generate an image for a dish using Stable Diffusion."""
    try:
        StableDiffusionPipeline, torch = get_diffusion_pipeline()
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Load the model (using a lightweight model for faster generation)
        model_id = "runwayml/stable-diffusion-v1-5"
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id, 
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            safety_checker=None,
            requires_safety_checker=False
        )
        pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
        
        # Create prompt from dish information
        dish_name = item.get("name", "food")
        description = item.get("short", "")
        image_prompt = item.get("image_prompt", "")
        
        if image_prompt:
            prompt = image_prompt
        else:
            prompt = f"high-resolution professional food photography of {dish_name}, {description}, beautifully plated, restaurant quality, soft lighting, appetizing"
        
        print(f"Generating: {dish_name}")
        
        # Generate image
        image = pipe(prompt, guidance_scale=7.5, num_inference_steps=20).images[0]
        
        # Save image
        safe_name = dish_name.lower().replace(" ", "_").replace("/", "_")
        image_path = os.path.join(output_dir, f"{safe_name}.png")
        image.save(image_path)
        return image_path
        
    except Exception as e:
        print(f"Error generating image for {item.get('name', 'unknown')}: {e}")
        return None


def generate_and_convert_to_ascii(item: dict, output_dir: str = "generated_images", ascii_width: int = 60, ascii_height: int = 30) -> str:
    """Generate an image for a dish and convert it to ASCII art."""
    
    # First try to generate the image
    image_path = generate_dish_image(item, output_dir)
    
    if image_path and os.path.exists(image_path):
        # Convert to ASCII
        ascii_art = image_to_ascii(image_path, ascii_width, ascii_height)
        return f"\n{ascii_art}\n"
    else:
        # Fallback to template-based ASCII if image generation fails
        return render_ascii_for_item(item)


def render_ascii_for_item(item: dict) -> str:
    key = (item.get("ascii_template") or "").strip().upper()
    if not key:
        return FALLBACK
    return TEMPLATES.get(key, FALLBACK)


def load_yaml(path: Path) -> dict:
    """Load YAML file."""
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)