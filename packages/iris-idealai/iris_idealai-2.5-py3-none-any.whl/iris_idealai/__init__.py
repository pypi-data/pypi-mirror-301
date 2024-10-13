import PIL.Image
from PIL import Image
import requests
from io import BytesIO
from .script import m_set, m_build, t_gen

class Iris:
    def __init__(self, model_name=None, api_key=None):
        if api_key:
            # Validate the API key using the security-codes endpoint
            validation_response = self._validate_api_key(api_key)
            
            if validation_response.get('status') == 'success':
                if validation_response.get('num_of_requests', 0) > 0:
                    validated_key = validation_response.get('key')
                    t_gen().configure(api_key=validated_key)  # Use the validated key
                    self.model = t_gen().GenerativeModel(model_name or m_set())
                    self.introduction = m_build()
                else:
                    # Raise an error if the request limit is reached
                    raise Exception("You have exceeded the limit of requests per day.")
            else:
                # Raise an error if the API key is invalid
                raise Exception(f"Invalid API key: {validation_response.get('message')}")
        else:
            # Handle the case where no API key is provided
            raise ValueError("API key must be provided. Please set the API key.")

    def _validate_api_key(self, api_key):
        if not api_key:
            raise ValueError("API key cannot be empty. Please provide a valid API key.")

        url = "https://practice.mchaexpress.com/iris/security-code.php"
        try:
            response = requests.post(url, json={"key": api_key})
            response.raise_for_status()

            response_data = response.json()
            
            if response_data.get('status') == 'error':
                raise ValueError(f"API key validation error: {response_data.get('message')}")

            return response_data
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error validating API key: {e}")
        if not api_key:
            raise ValueError("API key cannot be empty. Please provide a valid API key.")

        url = "https://practice.mchaexpress.com/iris/security-code.php"
        try:
            response = requests.post(url, json={"key": api_key})
            response.raise_for_status()

            response_data = response.json()
            
            if response_data.get('status') == 'error':
                raise ValueError(f"API key validation error: {response_data.get('message')}")

            return response_data
        
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error validating API key: {e}")

    def _introduce(self):
        return self.introduction

    def generate_text(self, prompt):
        final_prompt = self._introduce() + " " + prompt
        response = self.model.generate_content(final_prompt, stream=False)
        return response

    def generate_chunk_text(self, prompt):
        final_prompt = self._introduce() + " " + prompt
        response = self.model.generate_content(final_prompt, stream=True)

        # Collect all chunks of text
        chunks = []
        for chunk in response:
            if hasattr(chunk, 'text'):
                chunks.append(chunk.text)
            else:
                chunks.append(str(chunk))
        
        return "\n".join(chunks)
    
    def generate_custom_text(self, prompt, candidate_count=1, stop_sequences=None, max_output_tokens=100, temperature=1.0):
        if stop_sequences is None:
            stop_sequences = []
        
        # Create the GenerationConfig object with the provided parameters
        generation_config = t_gen().types.GenerationConfig(
            candidate_count=candidate_count,
            stop_sequences=stop_sequences,
            max_output_tokens=max_output_tokens,
            temperature=temperature
        )

        final_prompt = self._introduce() + " " + prompt
        response = self.model.generate_content(final_prompt, generation_config=generation_config)
        return self._process_response(response)
    
    def generate_image(self, prompt):
        encoded_prompt = requests.utils.quote(prompt)
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt} without pollination.ai mark/tag"
        
        try:
            # Fetch the image from the URL
            response = requests.get(url)
            if response.status_code == 200:
                image_blob = BytesIO(response.content)
                image = PIL.Image.open(image_blob)

                return image
            else:
                raise Exception("Failed to fetch image")

        except Exception as e:
            print(f"Error: {e}")
            return None

    def analyze_image(self, image_input, prompt="Tell me about this image"):
        # Check if image_input is a URL (starts with http or https)
        if isinstance(image_input, str) and (image_input.startswith("http://") or image_input.startswith("https://")):
            try:
                response = requests.get(image_input)
                if response.status_code == 200 and 'image' in response.headers['Content-Type']:
                    image = Image.open(BytesIO(response.content))
                else:
                    return "\n\nError: Unable to download the image or the URL is incorrect."
            except PIL.UnidentifiedImageError:
                return "\n\nError: The image could not be identified or processed."
        else:
            # Treat as a local file path
            try:
                image = Image.open(image_input)
            except FileNotFoundError:
                return "\n\nError: The file was not found at the specified path."
            except PIL.UnidentifiedImageError:
                return "\n\nError: The image could not be identified or processed."
        
        # Assuming the model can process the image object directly
        response = self.model.generate_content([prompt, image])
        analyzed_text = self._process_response(response)
        return f"{analyzed_text}"
        
    def _process_response(self, response):
        result = []
        for chunk in response:
            if hasattr(chunk, 'text'):
                result.append(chunk.text)
            else:
                result.append(str(chunk))
        return "\n".join(result)
