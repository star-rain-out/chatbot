import os
import requests


def main() -> None:
    """Test /api/social_media/generate with great_wall_real.jpg."""
    # Resolve image path relative to this file: ../great_wall_real.jpg
    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "..", "great_wall_real.jpg")

    if not os.path.exists(image_path):
        print("Image not found:", image_path)
        return

    url = "http://127.0.0.1:8000/api/social_media/generate"

    with open(image_path, "rb") as f:
        files = {"image": ("great_wall_real.jpg", f, "image/jpeg")}
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
        data = resp.json()
        print("generated_caption:\n", data.get("generated_caption"))
        print("image_analysis:", data.get("image_analysis"))
    except Exception:
        print("Body:", resp.text)


if __name__ == "__main__":
    main()

