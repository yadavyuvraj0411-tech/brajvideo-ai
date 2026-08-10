
import os
import requests
from pathlib import Path


OUTPUT_DIR = Path("generated_videos")
OUTPUT_DIR.mkdir(exist_ok=True)


def get_api_url():
    return os.environ.get("VIDEO_API_URL")


def get_api_key():
    return os.environ.get("VIDEO_API_KEY")


def check_configuration():
    api_url = get_api_url()
    api_key = get_api_key()

    if not api_url:
        return {
            "ready": False,
            "message": "VIDEO_API_URL is not configured."
        }

    if not api_key:
        return {
            "ready": False,
            "message": "VIDEO_API_KEY is not configured."
        }

    return {
        "ready": True,
        "message": "Video API configuration is ready."
    }


def create_video_request(prompt):
    api_url = get_api_url()
    api_key = get_api_key()

    if not api_url or not api_key:
        raise RuntimeError(
            "Video API is not configured."
        )

    response = requests.post(
        api_url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "prompt": prompt
        },
        timeout=60
    )

    response.raise_for_status()

    return response.json()


def save_video(video_bytes, filename):
    path = OUTPUT_DIR / filename

    with open(path, "wb") as file:
        file.write(video_bytes)

    return str(path)


if __name__ == "__main__":
    print("BrajVideo AI video worker")
    print(check_configuration())
