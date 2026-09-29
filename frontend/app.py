import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import os
import tempfile
from pathlib import Path

import gradio as gr
import requests
from dotenv import load_dotenv

from backend.utils.document_exporters import (
    format_txt,
    format_docx,
    format_pdf
)


# ---------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------

ROOT = Path(__file__).resolve().parents[1]

load_dotenv(ROOT / ".env")

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")

LOGO_PATH = os.getenv(
    "LOGO_PATH",
    str(ROOT / "assets" / "logo.svg")
)


# ---------------------------------------------------------
# DOCUMENT GENERATION
# ---------------------------------------------------------

def generate_document(
    document_type,
    parties,
    terms,
    dates
):
    """
    Send document information to FastAPI backend.
    """

    # Basic validation
    if not document_type:
        return (
            "",
            "❌ Please select a document type.",
            None,
            None,
            None
        )

    if not parties.strip():
        return (
            "",
            "❌ Please enter the parties.",
            None,
            None,
            None
        )

    if not terms.strip():
        return (
            "",
            "❌ Please enter the terms and conditions.",
            None,
            None,
            None
        )

    if not dates.strip():
        return (
            "",
            "❌ Please enter the effective date.",
            None,
            None,
            None
        )

    payload = {
        "document_type": document_type,
        "parties": parties,
        "terms": terms,
        "dates": dates
    }

    try:

        response = requests.post(
            f"{BACKEND_URL}/generate",
            json=payload,
            timeout=180
        )

        if response.status_code != 200:

            try:
                error_detail = response.json().get(
                    "detail",
                    "Unknown backend error."
                )

            except Exception:
                error_detail = response.text

            return (
                "",
                f"❌ Backend Error: {error_detail}",
                None,
                None,
                None
            )

        data = response.json()

        document = data.get(
            "content",
            ""
        )

        if not document:

            return (
                "",
                "❌ Gemini returned an empty document.",
                None,
                None,
                None
            )

        # -------------------------------------------------
        # CREATE DOWNLOAD FILES
        # -------------------------------------------------

        txt_bytes = format_txt(
            document
        )

        docx_bytes = format_docx(
            document,
            document_type,
            terms,
            LOGO_PATH
        )

        pdf_bytes = format_pdf(
            document,
            document_type,
            terms
        )

        txt_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".txt"
        )

        txt_file.write(
            txt_bytes
        )

        txt_file.close()

        docx_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".docx"
        )

        docx_file.write(
            docx_bytes
        )

        docx_file.close()

        pdf_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        )

        pdf_file.write(
            pdf_bytes
        )

        pdf_file.close()

        return (
            document,
            "✅ Document generated successfully!",
            txt_file.name,
            docx_file.name,
            pdf_file.name
        )

    except requests.exceptions.ConnectionError:

        return (
            "",
            "❌ Cannot connect to FastAPI backend. "
            "Make sure the backend is running on "
            f"{BACKEND_URL}",
            None,
            None,
            None
        )

    except requests.exceptions.Timeout:

        return (
            "",
            "❌ Request timed out. "
            "Gemini may be taking too long to respond.",
            None,
            None,
            None
        )

    except Exception as error:

        return (
            "",
            f"❌ Error: {error}",
            None,
            None,
            None
        )


# ---------------------------------------------------------
# CLEAR FORM
# ---------------------------------------------------------

def clear_form():

    return (
        "Rental Agreement",
        "",
        "",
        "",
        "",
        "Ready to create a new document.",
        None,
        None,
        None
    )


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

CUSTOM_CSS = """

body {
    background: #0e1117;
}

.gradio-container {
    max-width: 1200px !important;
    margin: auto !important;
}

#title {
    text-align: center;
    margin-bottom: 5px;
}

#subtitle {
    text-align: center;
    color: #a9afc1;
    margin-bottom: 25px;
}

textarea {
    font-size: 15px !important;
}

button {
    border-radius: 10px !important;
}

.generate-button {
    font-size: 18px !important;
    font-weight: bold !important;
}

.status-box {
    text-align: center;
    font-weight: bold;
}

"""

# ---------------------------------------------------------
# GRADIO INTERFACE
# ---------------------------------------------------------

with gr.Blocks(
    title="LegalEase AI",
    css=CUSTOM_CSS,
    theme=gr.themes.Soft(
        primary_hue="violet",
        neutral_hue="slate"
    )
) as app:

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    gr.Markdown(
        """
        # ⚖️ LegalEase AI
        """,
        elem_id="title"
    )

    gr.Markdown(
        """
        ### AI-Powered Legal Document Generator

        Create professional legal document drafts using AI.
        """,
        elem_id="subtitle"
    )

    gr.Markdown(
        """
        **Note:** Documents generated by AI are drafts and
        should be reviewed by a qualified legal professional.
        """
    )

    # -----------------------------------------------------
    # INPUT SECTION
    # -----------------------------------------------------

    with gr.Row():

        with gr.Column(scale=1):

            document_type = gr.Dropdown(
                choices=[
                    "Rental Agreement",
                    "Employment Agreement",
                    "Non-Disclosure Agreement",
                    "Service Agreement",
                    "Freelance Agreement",
                    "Partnership Agreement",
                    "Loan Agreement",
                    "Sale Agreement",
                    "General Legal Agreement"
                ],
                value="Rental Agreement",
                label="Document Type"
            )

            parties = gr.Textbox(
                label="Parties",
                placeholder=(
                    "Example:\n"
                    "Landlord: John Smith\n"
                    "Tenant: Jane Doe"
                ),
                lines=5
            )

            terms = gr.Textbox(
                label="Terms and Conditions",
                placeholder=(
                    "Enter the important terms "
                    "and conditions separated by semicolons."
                ),
                lines=8
            )

            dates = gr.Textbox(
                label="Effective Date",
                placeholder="Example: 1 October 2026",
                lines=2
            )

            with gr.Row():

                generate_button = gr.Button(
                    "⚖️ Generate Document",
                    variant="primary",
                    elem_classes="generate-button"
                )

                clear_button = gr.Button(
                    "Clear"
                )

    # -----------------------------------------------------
    # STATUS
    # -----------------------------------------------------

    status = gr.Markdown(
        "Ready to create your document.",
        elem_classes="status-box"
    )

    # -----------------------------------------------------
    # DOCUMENT OUTPUT
    # -----------------------------------------------------

    document_output = gr.Textbox(
    label="Generated Legal Document",
    placeholder=(
        "Your generated document will "
        "appear here..."
    ),
    lines=25
)
    # -----------------------------------------------------
    # DOWNLOAD SECTION
    # -----------------------------------------------------

    gr.Markdown(
        "## 📥 Download Document"
    )

    with gr.Row():

        txt_download = gr.File(
            label="Download TXT"
        )

        docx_download = gr.File(
            label="Download DOCX"
        )

        pdf_download = gr.File(
            label="Download PDF"
        )

    # -----------------------------------------------------
    # GENERATE BUTTON EVENT
    # -----------------------------------------------------

    generate_button.click(
        fn=generate_document,
        inputs=[
            document_type,
            parties,
            terms,
            dates
        ],
        outputs=[
            document_output,
            status,
            txt_download,
            docx_download,
            pdf_download
        ]
    )

    # -----------------------------------------------------
    # CLEAR BUTTON EVENT
    # -----------------------------------------------------

    clear_button.click(
        fn=clear_form,
        inputs=[],
        outputs=[
            document_type,
            parties,
            terms,
            dates,
            document_output,
            status,
            txt_download,
            docx_download,
            pdf_download
        ]
    )


# ---------------------------------------------------------
# RUN APPLICATION
# ---------------------------------------------------------

if __name__ == "__main__":

    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True
    )