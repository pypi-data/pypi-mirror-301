# Export the public API
from sema4ai.di_client.document_intelligence_client.document_intelligence_client import (
    _DocumentIntelligenceClient,
)

__version__ = "1.0.3"
version_info = [int(x) for x in __version__.split(".")]

class DocumentIntelligenceClient(_DocumentIntelligenceClient):
    """
    This is the public API for talking to the Document Intelligence API.

    See the package README for more information.
    """


__all__ = ["DocumentIntelligenceClient"]
