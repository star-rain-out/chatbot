import io

import requests
from PIL import Image


def main() -> None:
    """Simple manual test for /api/social_media/generate.

    It creates a small test image in memory and sends it to the running
    FastAPI backend, then prints the status code and JSON body.
    """

    url = "http://127.0.0.1:8000/api/social_media/generate"

    # Create a simple test image (orange square)
    img = Image.new("RGB", (64, 64), color=(255, 128, 0))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    files = {"image": ("test.jpg", buf, "image/jpeg")}
    data = {
        "platform": "instagram",
        "tone": "friendly",
        "hashtags_count": "5",
    }

    try:
        resp = requests.post(url, files=files, data=data, timeout=60)
    except Exception as e:
        print("Request failed:", repr(e))
        return

    print("Status:", resp.status_code)
    try:
        print("JSON:", resp.json())
    except Exception:
        print("Body:", resp.text)


if __name__ == "__main__":
    main()

