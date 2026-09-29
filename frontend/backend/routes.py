from fastapi import APIRouter, HTTPException

from backend.schemas import (
    DocumentRequest,
    DocumentResponse
)

from backend.ai_core.gemini_generator import (
    GeminiDocumentGenerator,
    GeminiConfigurationError,
    GeminiGenerationError
)


# Create the FastAPI router
router = APIRouter()


# Create Gemini generator
generator = GeminiDocumentGenerator()


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate_document(
    request: DocumentRequest
):
    """
    Generate a legal document using Gemini AI.
    """

    try:

        document = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates
        )

        return DocumentResponse(
            document_type=request.document_type,
            content=document
        )

    except GeminiConfigurationError as error:

        raise HTTPException(
            status_code=503,
            detail=str(error)
        )

    except GeminiGenerationError as error:

        raise HTTPException(
            status_code=502,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Unexpected server error: {error}"
        )