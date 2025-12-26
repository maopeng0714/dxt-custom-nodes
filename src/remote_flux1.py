import requests
import base64
import io
import torch
import numpy as np
from PIL import Image
from typing import List

class RemoteFlux1Generator:
    """ComfyUI node for generating images using remote Flux1 model"""
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "token": ("STRING", {
                    "default": "0V-_bBy9qhZ21hd0hf-otZ3PL6K6mUfb",
                    "multiline": False,
                    "placeholder": "API Authorization Token"
                }),
                "model": ("STRING", {
                    "default": "black-forest-labs/FLUX.1-schnell",
                    "multiline": False,
                    "placeholder": "Model name"
                }),
                "prompt": ("STRING", {
                    "default": "A cute flying cat",
                    "multiline": True,
                    "placeholder": "Prompt for image generation"
                }),
                "n": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 8,
                    "step": 1,
                    "placeholder": "Number of images to generate"
                }),
                "size": ("STRING", {
                    "default": "1024x1024",
                    "multiline": False,
                    "placeholder": "Image resolution (e.g., 1024x1024)"
                }),
                "api_url": ("STRING", {
                    "default": "https://api.kyle.moments8.com/dxtflux1schnell/v1/images/generations",
                    "multiline": False,
                    "placeholder": "API endpoint URL"
                })
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("IMAGE", "url")
    FUNCTION = "generate_images"
    CATEGORY = "多信通自定义节点"
    
    def generate_images(self, token, model, prompt, n, size, api_url):
        """Generate images using remote Flux1 model"""
        try:
            # Prepare request headers and body
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            
            payload = {
                "model": model,
                "prompt": prompt,
                "n": n,
                "size": size
            }
            
            # Send request to remote API
            print(f"Sending request to {api_url} with payload: {payload}")
            response = requests.post(api_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            # Parse response
            result = response.json()
            print(f"Received response: {result}")
            
            # Extract base64 images from response
            images = []
            for img_data in result.get("data", []):
                base64_str = img_data.get("b64_json", "")
                if base64_str:
                    # Decode base64 string to image
                    img_bytes = base64.b64decode(base64_str)
                    img = Image.open(io.BytesIO(img_bytes))
                    
                    # Convert PIL image to torch tensor
                    img_array = np.array(img).astype(np.float32) / 255.0
                    # Convert HWC to CHW format
                    img_tensor = torch.from_numpy(img_array).permute(2, 0, 1)
                    images.append(img_tensor)
            
            if not images:
                raise ValueError("No images generated from API response")
            
            # Stack images into a batch tensor
            batch_tensor = torch.stack(images)
            
            # Return images tensor and API URL
            return (batch_tensor, api_url)
            
        except Exception as e:
            print(f"Error generating images: {str(e)}")
            raise e
