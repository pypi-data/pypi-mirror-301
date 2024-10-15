from typing import Optional, Union
from sema4ai.di_client.document_intelligence_client.models import (
    DocumentWorkItem, DocumentFormat,
    RawDocumentContent, ExtractedDocumentContent, TransformedDocumentContent, ComputedDocumentContent,
    DocumentFormatState
)
from sema4ai.di_client.document_intelligence_client.models.content_state import ContentState
from sema4ai.di_client.document_intelligence_client.models.get_document_content200_response import GetDocumentContent200Response
from sema4ai.di_client.document_intelligence_client.models.doc_type import DocType
from sema4ai.di_client.document_intelligence_client.api.default_api import DefaultApi as DocumentIntelligenceDefaultApi
from sema4ai.di_client.document_intelligence_client.exceptions import ApiException
from sema4ai.di_client.agents_events_publisher.models import PostWorkItemsCompleteStageRequest
from sema4ai.di_client.agents_events_publisher.api.default_api import DefaultApi as WorkItemsDefaultApi
import logging
import os
import re


logging.basicConfig(level=logging.INFO)


class _DocumentIntelligenceClient:
    def __init__(self, workspace_id: Optional[str] = None):
        di_service_url = os.getenv('DOCUMENT_INTELLIGENCE_SERVICE_URL')
        agents_events_service_url = os.getenv('AGENTS_EVENTS_SERVICE_URL')

        # Check if required environment variables are set, throw error if not
        if not di_service_url:
            raise ValueError("Environment variable 'DOCUMENT_INTELLIGENCE_SERVICE_URL' is not set.")
        if not agents_events_service_url:
            raise ValueError("Environment variable 'AGENTS_EVENTS_SERVICE_URL' is not set.")

        # If di_service_url contains '/documents', strip it to form the base_url
        if di_service_url.endswith('/documents'):
            self.base_url = di_service_url.rsplit('/documents', 1)[0]
            logging.info(f"Stripping '/documents' from service URL. Base URL set to: {self.base_url}")
        else:
            # If di_service_url is localhost or doesn't contain '/documents'
            self.base_url = di_service_url
            logging.info(f"Base URL set to: {self.base_url}")

        # Extract workspace ID or log an error if extraction fails
        self.workspace_id = workspace_id if workspace_id else self._get_tenant_id_from_url()
        if not self.workspace_id:
            logging.error(f"Failed to extract workspace ID from URL: {self.base_url}, or from the arguments")
            raise ValueError("Workspace ID is not set")

        # Initialize the clients
        self.documents_data_client = DocumentIntelligenceDefaultApi()
        self.work_items_client = WorkItemsDefaultApi()

        # Check if the base URL is local
        def is_local_url(url):
            from urllib.parse import urlparse
            local_addresses = ['localhost', '127.0.0.1', '0.0.0.0']
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname
            return hostname in local_addresses

        # If the base URL is not local, configure the client URLs
        if not is_local_url(self.base_url):
            # Set the base URLs for the clients
            self.documents_data_client.api_client.configuration.host = di_service_url
            self.work_items_client.api_client.configuration.host = agents_events_service_url
            logging.info(f"Documents Data Client URL set to: {di_service_url}")
            logging.info(f"Work Items Client URL set to: {agents_events_service_url}")
        else:
            self.documents_data_client.api_client.configuration.host = self.base_url
            self.work_items_client.api_client.configuration.host = self.base_url
            logging.info(f"Using local base URL: {self.base_url}")


    def _get_tenant_id_from_url(self):
        """
        The workspace ID appears after the 'workspace-id/' part in the URL.

        Returns:
        - workspace ID (str): The extracted tenant ID.
        """
        # Use regex to extract the tenant ID
        match = re.search(r"workspace-id/([a-f0-9-]+)/", self.base_url)
        if match:
            workspace_id = match.group(1)
            return workspace_id
        else:
            print("Workspace ID not found in URL.")
            return None

    def close(self):
        pass

    def get_document_work_item(self, document_id: str) -> Optional[DocumentWorkItem]:
        try:
            # Directly call the API method
            data = self.documents_data_client.get_document_work_item(
                workspace_id=self.workspace_id,
                document_id=document_id,
            )
            if data:
                logging.debug(f"Received data for document_id {document_id}: {data}")
                return data
            else:
                logging.warning(f"No data received for document_id {document_id}")
                return None
        except ApiException as e:
            logging.error(f"API error occurred while getting document work item: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None

    def get_document_type(self, document_type_name: str) -> Optional[DocType]:
        try:
            data = self.documents_data_client.get_document_type(
                workspace_id=self.workspace_id,
                document_type_name=document_type_name
            )
            if data:
                logging.debug(f"Received document type: {data}")
                return data
            else:
                logging.warning(f"No data received for document_type_name {document_type_name}")
                return None
        except ApiException as e:
            logging.error(f"API error occurred while getting document type: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None

    def get_document_format(self, document_type_name: str, document_class_name: str) -> Optional[DocumentFormat]:
        try:
            data = self.documents_data_client.get_document_format(
                workspace_id=self.workspace_id,
                document_type_name=document_type_name,
                document_format_name=document_class_name
            )
            if data:
                # Ensure that the state is parsed correctly
                data.state = DocumentFormatState(data.state)
                logging.debug(f"Received document format: {data}")
                return data
            else:
                logging.warning(
                    f"No data received for document_type_name {document_type_name} and document_class_name {document_class_name}"
                )
                return None
        except ApiException as e:
            logging.error(f"API error occurred while getting document format: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None

    def store_extracted_content(self, content: ExtractedDocumentContent) -> None:
        try:
            self.documents_data_client.post_store_extracted_content(
                workspace_id=self.workspace_id,
                extracted_document_content=content
            )
            logging.info(f"Successfully stored extracted content for workspace {self.workspace_id}")
        except ApiException as e:
            logging.error(f"API error occurred while storing extracted content: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    def store_transformed_content(self, content: TransformedDocumentContent) -> None:
        try:
            self.documents_data_client.post_store_transformed_content(
                workspace_id=self.workspace_id,
                transformed_document_content=content
            )
            logging.info(f"Successfully stored transformed content for workspace {self.workspace_id}")
        except ApiException as e:
            logging.error(f"API error occurred while storing transformed content: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")

    def get_document_content(
        self, document_id: str, content_state: ContentState
    ) -> Optional[
        Union[
            RawDocumentContent,
            ExtractedDocumentContent,
            TransformedDocumentContent,
            ComputedDocumentContent
        ]
    ]:
        try:
            response: GetDocumentContent200Response = self.documents_data_client.get_document_content(
                workspace_id=self.workspace_id,
                document_id=document_id,
                content_state=content_state.value
            )
            return response.actual_instance
        except ApiException as e:
            logging.error(f"API error occurred while getting document content: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred while getting document content: {e}")
            return None

    def remove_document_content(self, document_id: str, content_state: ContentState) -> None:
        try:
            self.documents_data_client.remove_document_content(
                workspace_id=self.workspace_id,
                document_id=document_id,
                content_state=content_state.value
            )
            logging.info(
                f"Document content removed successfully for document_id {document_id} and content_state {content_state}"
            )
        except ApiException as e:
            logging.error(f"API error occurred while removing document content: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred while removing document content: {e}")

    def store_computed_content(self, content: ComputedDocumentContent) -> None:
        try:
            self.documents_data_client.post_store_computed_content(
                workspace_id=self.workspace_id,
                computed_document_content=content
            )
            logging.info(f"Successfully stored computed content for workspace {self.workspace_id}")
        except ApiException as e:
            logging.error(f"API error occurred while storing computed content: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred while storing computed content: {e}")

    def work_items_complete_stage(
            self,
            work_item_id: str,
            status: str,
            status_reason: Optional[str] = None,
            log_details_path: Optional[str] = None
    ):
        """Completes the current stage of a work item and initiates the next stage."""

        # Validate that the status is either 'SUCCESS' or 'FAILURE'
        if status not in ['SUCCESS', 'FAILURE']:
            logging.error(f"Invalid status: {status}. Must be 'SUCCESS' or 'FAILURE'.")
            return None

        # Create the request data with the required fields
        request_data = PostWorkItemsCompleteStageRequest(
            tenant_id=self.workspace_id,
            work_item_id=work_item_id,
            status=status,
            status_reason=status_reason,
            log_details_path=log_details_path
        )

        try:
            # Call the generated API method to complete the work item stage
            response = self.work_items_client.post_work_items_complete_stage(
                post_work_items_complete_stage_request=request_data
            )
            logging.info(
                f"Successfully completed stage for work_item_id {work_item_id}, moving to next stage."
            )
            return response
        except ApiException as e:
            logging.error(f"API error occurred while completing stage for work_item_id {work_item_id}: {e}")
            return None
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            return None

