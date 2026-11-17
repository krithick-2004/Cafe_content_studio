import os

import requests
from dotenv import load_dotenv
from fastapi import HTTPException


load_dotenv()

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

STABILITY_IMAGE_URL = (
    "https://api.stability.ai/v2beta/stable-image/generate/core"
)


def generate_image(prompt: str, aspect_ratio: str = "16:9") -> bytes:
    """
    Generate a PNG image using Stability AI Stable Image Core.
    Returns the generated image as bytes for the FastAPI Response.
    """

    if not STABILITY_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="STABILITY_API_KEY is missing from the .env file."
        )

    if not prompt or not prompt.strip():
        raise HTTPException(
            status_code=400,
            detail="Image prompt cannot be empty."
        )

    allowed_ratios = {
        "16:9", "1:1", "3:2", "2:3",
        "4:5", "5:4", "9:16", "9:21"
    }

    if aspect_ratio not in allowed_ratios:
        aspect_ratio = "16:9"

    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Accept": "image/*"
    }

    form_data = {
        "prompt": prompt.strip(),
        "aspect_ratio": aspect_ratio,
        "output_format": "png"
    }

    try:
        response = requests.post(
            STABILITY_IMAGE_URL,
            headers=headers,
            files={"none": (None, "")},
            data=form_data,
            timeout=120
        )

        if response.status_code != 200:
            try:
                error_data = response.json()
                error_message = (
                    error_data.get("message")
                    or error_data.get("name")
                    or str(error_data)
                )
            except ValueError:
                error_message = response.text[:1000]

            status_code = (
                response.status_code
                if 400 <= response.status_code < 500
                else 502
            )

            raise HTTPException(
                status_code=status_code,
                detail=(
                    f"Stability AI image generation failed: "
                    f"{error_message}"
                )
            )

        return response.content

    except requests.Timeout:
        raise HTTPException(
            status_code=504,
            detail="Stability AI timed out. Please try again."
        )

    except requests.RequestException as error:
        raise HTTPException(
            status_code=502,
            detail=f"Could not connect to Stability AI: {error}"
        )