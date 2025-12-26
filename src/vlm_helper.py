import re
import requests


class VLMHelperNode:
    """ComfyUI node for VLM prompt assistant using Qwen3-30B-A3B"""

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "placeholder": "Enter your prompt text here"
                }),
                "model": ("STRING", {
                    "default": "Qwen/Qwen3-30B-A3B",
                    "multiline": False,
                    "placeholder": "Model name"
                }),
                "system_prompt": ("STRING", {
                    "default": "你是一个专业的 SDXL 提示词优化专家。你的任务是将用户输入的任意文字（可能是中文描述、故事片段或简单想法）转换为详细、英文的 SDXL提示词。输出格式必须严格遵守以下规则： 以英文撰写，全长 50-150 词。结构：主体描述, 细节 (details: lighting, colors, composition) ,风格/氛围 (style: e.g., realistic, cyberpunk),质量提升 (quality: highly,detailed, 8k, masterpiece)。使用权重如 (element:1.2) 强调关键部分。避免负面提示（negative prompts），只输出正面提示。如果输入是中文，先翻译成英文再优化。输出只包含提示词本身，无额外解释。/no_think",
                    "multiline": True,
                    "placeholder": "System prompt for the VLM model"
                }),
                "api_key": ("STRING", {
                    "default": "QsX1wAPBSOETsGOcFOP-DKENegm52HOG",
                    "multiline": False,
                    "placeholder": "API Authorization Token"
                }),
                "api_url": ("STRING", {
                    "default": "https://dxt104.intra.moments8.com/v1/chat/completions",
                    "multiline": False,
                    "placeholder": "API endpoint URL"
                })
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("processed_prompt",)
    FUNCTION = "process_prompt"
    CATEGORY = "多信通自定义节点"

    def process_prompt(self, prompt: str, model: str, system_prompt: str, api_key: str, api_url: str) -> tuple:
        """Process prompt through VLM assistant and clean the result"""
        try:

            # Prepare the API request payload
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False,
                "temperature": 0.7,
                "top_p": 0.8,
                "frequency_penalty": 0,
                "max_tokens": 4096,
                "top_k": 20
            }

            # Prepare request headers
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            print(f"Sending request to {api_url} with prompt: {prompt[:100]}...")

            # Make API request
            response = requests.post(api_url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()

            result = response.json()
            print(f"Received response: {result}")

            # Extract content from response (based on return.json structure)
            if "choices" in result and len(result["choices"]) > 0:
                message_content = result["choices"][0]["message"]["content"]

                # Clean the content by removing <thinking> tags and their content
                cleaned_prompt = self._remove_thinking_tags(message_content)

                print(f"Cleaned prompt: {cleaned_prompt}")
                return (cleaned_prompt,)
            else:
                return (f"Error: No response from VLM API",)

        except Exception as e:
            print(f"Error processing prompt with VLM: {str(e)}")
            return (f"Error: {str(e)}",)

    def _remove_thinking_tags(self, text: str) -> str:
        """Remove thinking tags and their content from text"""
        # Remove various thinking tag formats
        # Pattern 1: <thinking>...</thinking>
        pattern1 = r'<thinking>.*?</thinking>'
        cleaned = re.sub(pattern1, '', text, flags=re.DOTALL)

        # Pattern 2: <think>...</think>
        pattern2 = r'<think>.*?</think>'
        cleaned = re.sub(pattern2, '', cleaned, flags=re.DOTALL)

        # Pattern 3: | standalone symbol (sometimes appears as tag marker)
        cleaned = cleaned.replace('|', '')

        # Clean up extra whitespace and newlines
        cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)
        cleaned = cleaned.strip()

        return cleaned
