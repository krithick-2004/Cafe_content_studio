
import json
import os
from dotenv import load_dotenv
from groq import Groq

from backend.models.schemas import CreativeBrief


# Load environment variables
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY is missing. Please check your .env file.")


# Initialize Groq client
client = Groq(api_key=groq_api_key)


def generate_creative_concept(
    content: str,
    source_type: str = "text"
) -> CreativeBrief:

    if source_type == "pdf":
        user_content = (
            "The following content was extracted from a PDF creative brief. "
            "Analyze the complete content and transform it into a professional "
            "structured creative brief.\n\n"
            f"PDF CONTENT:\n{content}"
        )
    else:
        user_content = content

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are Ascent AI, an expert AI creative director "
                    "and brand strategist. "

                    "Your task is to transform the user's input into a "
                    "professional, imaginative, and detailed creative brief. "

                    "Preserve the user's important requirements and organize "
                    "them into a structured creative concept. "

                    "For business concepts such as coffee shops, restaurants, "
                    "and retail stores, focus on brand identity, customer "
                    "experience, atmosphere, visual design, and marketing appeal. "

                    "Make every field specific, practical, and useful for "
                    "future AI image generation, branding, and design. "

                    "Do not invent unnecessary business details."
                )
            },
            {
                "role": "user",
                "content": user_content
            }
        ],

        temperature=0.7,
        max_completion_tokens=2000,
        reasoning_effort="low",

        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "creative_brief",
                "strict": True,

                "schema": {
                    "type": "object",

                    "properties": {
                        "name": {
                            "type": "string"
                        },

                        "tagline": {
                            "type": "string"
                        },

                        "concept": {
                            "type": "string"
                        },

                        "mood": {
                            "type": "string"
                        },

                        "visual_style": {
                            "type": "string"
                        },

                        "target_audience": {
                            "type": "string"
                        },

                        "key_features": {
                            "type": "array",
                            "items": {
                                "type": "string"
                            }
                        }
                    },

                    "required": [
                        "name",
                        "tagline",
                        "concept",
                        "mood",
                        "visual_style",
                        "target_audience",
                        "key_features"
                    ],

                    "additionalProperties": False
                }
            }
        }
    )

    # Extract AI response
    response_content = response.choices[0].message.content

    # Convert JSON response into Python dictionary
    data = json.loads(response_content)

    # Validate and return CreativeBrief object
    return CreativeBrief(**data)


# -----------------------------------------
# TESTING: NEW COFFEE SHOP CREATIVE BRIEF
# -----------------------------------------

if __name__ == "__main__":

    coffee_shop_prompt = """
    Create a creative concept for launching a new premium coffee shop
    named Brew Haven.

    The coffee shop should have a modern, aesthetic, and welcoming
    atmosphere where customers can enjoy high-quality coffee,
    delicious snacks, and a comfortable environment.

    Brand Identity:
    Create a memorable brand identity with a stylish name and tagline.

    Concept:
    A modern coffee shop combining specialty coffee, relaxing spaces,
    and a premium customer experience.

    Mood:
    Warm, cozy, relaxing, welcoming, sophisticated, and youthful.

    Visual Style:
    Minimalist interior design, warm wooden furniture, soft ambient
    lighting, earthy colors, elegant typography, modern coffee
    equipment, and aesthetic coffee presentation.

    Target Audience:
    College students, young professionals, freelancers,
    coffee lovers, and people looking for a comfortable place
    to relax or work.

    Key Features:
    1. Premium freshly brewed coffee.
    2. Signature coffee drinks and seasonal beverages.
    3. Modern and aesthetic interior design.
    4. Comfortable seating and free Wi-Fi.
    5. Fresh bakery items and delicious snacks.
    6. Instagram-friendly photography corners.
    7. Friendly customer service and takeaway options.

    Make the creative brief professional, imaginative,
    visually appealing, and suitable for future AI image
    generation, branding, logo design, interior design,
    and marketing campaigns.
    """

    result = generate_creative_concept(
        content=coffee_shop_prompt,
        source_type="text"
    )

    print("\n========== ASCENT AI CREATIVE BRIEF ==========\n")

    print(result.model_dump_json(indent=4))
