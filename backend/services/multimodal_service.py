
import json
import os

from dotenv import load_dotenv
from groq import Groq
from backend.models.schemas import CreativeBrief


# Load environment variables
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)


def generate_multimodal_creative_brief(
    idea: str = "",
    voice_transcript: str = "",
    pdf_content: str = "",
    reference_analysis: dict | None = None
) -> CreativeBrief:

    context_parts = []

    if idea.strip():
        context_parts.append(
            "TEXT IDEA:\n" + idea.strip()
        )

    if voice_transcript.strip():
        context_parts.append(
            "VOICE TRANSCRIPT:\n" + voice_transcript.strip()
        )

    if pdf_content.strip():
        context_parts.append(
            "PDF CONTENT:\n" + pdf_content.strip()
        )

    if reference_analysis:
        context_parts.append(
            "REFERENCE IMAGE ANALYSIS:\n"
            + json.dumps(reference_analysis)
        )

    combined_context = "\n\n".join(context_parts)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are Ascent AI, an expert coffee shop "
                    "creative director, cafe branding specialist, "
                    "and interior design consultant. "

                    "Your task is to transform the user's information "
                    "into a professional creative brief for launching "
                    "a new coffee shop or cafe. "

                    "Focus exclusively on coffee shop concepts, "
                    "cafe branding, coffee products, customer experience, "
                    "interior design, and cafe marketing. "

                    "Combine all relevant information from text ideas, "
                    "voice transcripts, PDF documents, and reference "
                    "image analysis into one coherent creative brief. "

                    "BRAND IDENTITY: "
                    "Create an attractive, memorable coffee shop name "
                    "and a unique tagline that reflects the brand identity. "

                    "CONCEPT: "
                    "Describe the coffee shop theme, specialty, "
                    "unique selling points, customer experience, "
                    "and overall business concept. "

                    "MOOD: "
                    "Describe the atmosphere using suitable emotions "
                    "such as cozy, warm, relaxing, modern, premium, "
                    "minimalist, energetic, or welcoming. "

                    "VISUAL STYLE: "
                    "Describe the interior design, color palette, "
                    "lighting, furniture, wall decorations, coffee "
                    "counter, typography, logo direction, and overall "
                    "visual appearance. "

                    "TARGET AUDIENCE: "
                    "Identify suitable customers such as college "
                    "students, young professionals, freelancers, "
                    "families, and coffee lovers. Adapt the audience "
                    "to the user's actual requirements. "

                    "KEY FEATURES: "
                    "Provide specific coffee shop features such as "
                    "specialty coffee, signature beverages, bakery "
                    "items, comfortable seating, free Wi-Fi, takeaway "
                    "services, Instagram-friendly spaces, and "
                    "customer-friendly facilities. Choose features "
                    "that match the user's idea. "

                    "Preserve all important user requirements. "
                    "Use reference images as visual inspiration rather "
                    "than copying them literally. "

                    "Resolve contradictions by prioritizing explicit "
                    "user requirements. Do not invent unsupported "
                    "details. "

                    "Make the creative brief imaginative, professional, "
                    "specific, and useful for future AI image generation, "
                    "logo design, cafe interior visualization, "
                    "branding, and marketing campaigns. "

                    "Do not mention internal sources or the generation "
                    "process. Return only the requested JSON structure."
                )
            },
            {
                "role": "user",
                "content": (
                    combined_context
                    if combined_context
                    else "Create a unique, modern, and welcoming "
                         "coffee shop creative concept."
                )
            }
        ],

        temperature=0.7,
        max_completion_tokens=2000,
        reasoning_effort="low",

        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "coffee_shop_creative_brief",
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
    content = response.choices[0].message.content

    # Convert JSON into Python dictionary
    data = json.loads(content)

    # Return validated CreativeBrief object
    return CreativeBrief(**data)
