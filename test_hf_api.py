import requests
import io
from PIL import Image

def test_api():
    # Create a simple image
    img = Image.new('RGB', (100, 100), color = 'red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()

    # API_URL = "https://api-inference.huggingface.co/models/mmgyorke/vit-world-landmarks"
    API_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"
    
    print(f"Testing {API_URL}...")
    response = requests.post(API_URL, data=img_byte_arr)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

if __name__ == "__main__":
    test_api()
