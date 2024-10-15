from http import HTTPStatus
from unittest.mock import patch

import httpx
import pytest

from stellanow_api_internals.clients.workflow_manager_client import WorkflowManagerClient


@pytest.fixture
def mock_workflow_client():
    """Factory fixture that requires a custom response."""

    def create_mock_client(custom_response):
        if not custom_response:
            raise ValueError("You must provide a custom response")

        def mock_transport(request):
            return httpx.Response(HTTPStatus.OK, json=custom_response)

        transport = httpx.MockTransport(mock_transport)
        client = httpx.Client(transport=transport)

        with patch.object(WorkflowManagerClient, "authenticate", return_value=None):
            workflow_client = WorkflowManagerClient(
                base_url="https://mockapi.com",
                username="user",
                password="pass",
                organization_id="org_id",
                project_id="8db9f3bf-bea1-46dc-9364-e9dc4f2fa01f",
                client=client,
            )
            workflow_client.auth_token = "mocked_token"  # Mock token
            return workflow_client

    return create_mock_client
