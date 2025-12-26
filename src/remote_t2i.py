import requests
import base64
import io
import torch
import numpy as np
from PIL import Image
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed

class RemoteT2iGenerator:
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
                "size": ("STRING", {
                    "default": "1024x1024",
                    "multiline": False,
                    "placeholder": "Image resolution (e.g., 1024x1024)"
                }),
                "batch_size": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 10,
                    "step": 1,
                    "placeholder": "Number of concurrent requests"
                }),
                "api_url": ("STRING", {
                    "default": "https://api.kyle.moments8.com/dxtflux1schnell/v1/images/generations",
                    "multiline": False,
                    "placeholder": "API endpoint URL"
                })
            },
        }
    
    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("IMAGE", "url")
    FUNCTION = "generate_images"
    CATEGORY = "多信通自定义节点"
    
    def generate_images(self, token, model, prompt, size, batch_size, api_url):
        """Generate images using remote Flux1 model with concurrent requests"""
        try:
            # Prepare request headers
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }

            # Function to handle a single API request
            def single_request(request_id):
                payload = {
                    "model": model,
                    "prompt": prompt,
                    "n": 1,  # Each request generates 1 image
                    "size": size
                }

                print(f"Request {request_id}: Sending request to {api_url} with payload: {payload}")
                response = requests.post(api_url, headers=headers, json=payload, timeout=60)
                response.raise_for_status()

                result = response.json()
                print(f"Request {request_id}: Received response")

                # Extract base64 images from response
                for img_data in result.get("data", []):
                    base64_str = img_data.get("b64_json", "")
                    if base64_str:
                        # Decode base64 string to image
                        img_bytes = base64.b64decode(base64_str)
                        img = Image.open(io.BytesIO(img_bytes))

                        print(f"Request {request_id}: PIL image size: {img.size}, mode: {img.mode}")

                        # Convert PIL image to torch tensor
                        img_array = np.array(img).astype(np.float32) / 255.0
                        print(f"Request {request_id}: Image array shape: {img_array.shape}, dtype: {img_array.dtype}")

                        # Create tensor with batch dimension (BHWC format)
                        img_tensor = torch.from_numpy(img_array)
                        print(f"Request {request_id}: Image tensor shape: {img_tensor.shape}, dtype: {img_tensor.dtype}")

                        # Ensure tensor is contiguous and on CPU
                        img_tensor = img_tensor.contiguous().cpu()

                        return img_tensor

                raise ValueError(f"No images generated from API response for request {request_id}")

            # Execute concurrent requests
            images = []
            with ThreadPoolExecutor(max_workers=batch_size) as executor:
                # Submit all requests
                futures = [executor.submit(single_request, i) for i in range(batch_size)]

                # Collect results as they complete
                for future in as_completed(futures):
                    try:
                        img_tensor = future.result()
                        images.append(img_tensor)
                    except Exception as e:
                        print(f"Request failed: {str(e)}")
                        raise e

            if not images:
                raise ValueError("No images generated from any request")

            print(f"Number of images collected: {len(images)}")
            for i, img in enumerate(images):
                print(f"Image {i} shape: {img.shape}, dtype: {img.dtype}, device: {img.device}")

            # Stack images into a batch tensor
            batch_tensor = torch.stack(images)
            print(f"Final batch tensor shape: {batch_tensor.shape}, dtype: {batch_tensor.dtype}")
            print(f"Final batch tensor min: {batch_tensor.min()}, max: {batch_tensor.max()}")
            print(f"Final batch tensor is_contiguous: {batch_tensor.is_contiguous()}")

            # Return images tensor and API URL
            return (batch_tensor, api_url)

        except Exception as e:
            print(f"Error generating images: {str(e)}")
            raise e
