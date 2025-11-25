import sys
import os
import base64
from PIL import Image
import io

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

try:
    from routers.tools_social_media import analyze_image_with_base64
    print("Successfully imported analyze_image_with_base64")
except Exception as e:
    print(f"Failed to import: {e}")
    sys.exit(1)

def test_social_media_analysis():
    # Create a dummy image
    img = Image.new('RGB', (100, 100), color = 'blue')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    img_data = img_byte_arr.getvalue()
    
    base64_str = base64.b64encode(img_data).decode('utf-8')
    
    print("Testing analyze_image_with_base64...")
    result = analyze_image_with_base64(base64_str)
    
    print("Result:")
    print(result)
    
    if isinstance(result, dict):
        if result.get("source") == "serpapi":
            print("SUCCESS: Used SerpApi!")
        else:
            print("WARNING: Fallback to local heuristic (or SerpApi failed to find description)")
    else:
        print("FAILED: Result is not a dict")

if __name__ == "__main__":
    test_social_media_analysis()
