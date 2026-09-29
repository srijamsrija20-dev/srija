import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ---------------------------------------------------------
# LOAD .ENV FROM PROJECT ROOT
# ---------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]
ENV_FILE = ROOT / ".env"

load_dotenv(
    ENV_FILE,
    override=True
)


# ---------------------------------------------------------
# CUSTOM ERRORS
# ---------------------------------------------------------

class GeminiConfigurationError(Exception):
    pass


class GeminiGenerationError(Exception):
    pass


# ---------------------------------------------------------
# GEMINI DOCUMENT GENERATOR
# ---------------------------------------------------------

class GeminiDocumentGenerator:

    def __init__(self):

        self.api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        self.model = os.getenv(
            "GEMINI_MODEL",
            "gemini-3.8-flash"
        )

        self.client = None

        if self.api_key:
            self.client = genai.Client(
                api_key=self.api_key
            )

    # -----------------------------------------------------
    # CHECK CONFIGURATION
    # -----------------------------------------------------

    @property
    def configured(self):

        return bool(
            self.api_key
            and self.client
        )

    # -----------------------------------------------------
    # GENERATE DOCUMENT
    # -----------------------------------------------------

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        dates
    ):

        if not self.configured:

            raise GeminiConfigurationError(
                "GEMINI_API_KEY is missing. "
                "Please add your Gemini API key "
                "to the .env file."
            )

        prompt = f"""
You are LegalEase, an AI-powered legal
document drafting assistant.

Create a professional legal document draft.

Document Type:
{document_type}

Parties:
{parties}

Effective Date:
{dates}

Terms and Conditions:
{terms}

Instructions:

1. Use only the information provided.
2. Do not invent names, dates, amounts,
   addresses or facts.
3. If important information is missing,
   use [MISSING INFORMATION].
4. Organize the document into clear sections.
5. Use professional legal language.
6. Include appropriate signature sections.
7. Return only the document.
8. This is an AI-generated draft and should
   be reviewed by a qualified legal professional.
"""

        try:

            response = None

            # Retry temporary Gemini 503 errors
            for attempt in range(3):

                try:

                    response = self.client.models.generate_content(
                        model=self.model,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            temperature=0.2,
                            max_output_tokens=8192
                        )
                    )

                    break

                except Exception as error:

                    error_text = str(error)

                    if (
                        "503" in error_text
                        or "UNAVAILABLE" in error_text
                    ):

                        if attempt < 2:

                            wait_time = 3 * (attempt + 1)

                            time.sleep(
                                wait_time
                            )

                            continue

                    raise

            if response is None:

                raise GeminiGenerationError(
                    "Gemini did not return a response."
                )

            if not response.text:

                raise GeminiGenerationError(
                    "Gemini returned an empty response."
                )

            return response.text.strip()

        except GeminiGenerationError:

            raise

        except Exception as error:

            raise GeminiGenerationError(
                f"Gemini API error: {error}"
            )