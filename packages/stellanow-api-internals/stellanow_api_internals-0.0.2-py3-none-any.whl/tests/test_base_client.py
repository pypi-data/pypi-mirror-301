import unittest
from datetime import datetime
from http import HTTPStatus
from unittest.mock import patch

import httpx

from stellanow_api_internals.auth.keycloak_auth import KeycloakAuth
from stellanow_api_internals.clients.base_api_client import StellanowBaseAPIClient


class TestStellanowBaseAPIClient(unittest.TestCase):

    def setUp(self):
        self.patcher = patch.object(
            KeycloakAuth,
            "get_token",
            return_value={"access_token": "mock_access_token", "refresh_token": "mock_refresh_token"},
        )
        self.mock_get_token = self.patcher.start()

        self.patcher_refresh = patch.object(
            KeycloakAuth,
            "refresh_token",
            return_value={"access_token": "mock_access_token", "refresh_token": "mock_refresh_token"},
        )
        self.mock_refresh_token = self.patcher_refresh.start()

    def tearDown(self):
        self.patcher.stop()
        self.patcher_refresh.stop()

    def create_mock_transport(self, json_data, status_code=HTTPStatus.OK):
        """Helper function to create a MockTransport with specified JSON response."""
        return httpx.MockTransport(lambda request: httpx.Response(status_code, json=json_data))

    def test_authenticate(self):
        transport = self.create_mock_transport(json_data={"key": "value"})
        client = StellanowBaseAPIClient(
            base_url="https://api.stellanow.com",
            username="test_user",
            password="test_password",
            organization_id="test_org",
            client=httpx.Client(transport=transport),  # Pass the mocked transport
        )

        client.authenticate()
        self.assertEqual(client.auth_token, "mock_access_token")
        self.assertEqual(client.refresh_token, "mock_refresh_token")

    def test_make_request_get(self):
        transport = self.create_mock_transport(json_data={"details": {"key": "value"}})
        client = StellanowBaseAPIClient(
            base_url="https://api.stellanow.com",
            username="test_user",
            password="test_password",
            organization_id="test_org",
            client=httpx.Client(transport=transport),  # Pass the mocked transport
        )

        response = client._make_request(url="https://api.stellanow.com/test", method="GET")
        self.assertEqual(response, {"key": "value"})

    def test_handle_dates(self):
        # Simulate response with date fields
        mock_data = {
            "details": {"createdAt": "2024-03-06T18:22:19.335921Z", "updatedAt": "2024-06-27T08:28:40.973269Z"}
        }
        transport = self.create_mock_transport(json_data=mock_data)
        client = StellanowBaseAPIClient(
            base_url="https://api.stellanow.com",
            username="test_user",
            password="test_password",
            organization_id="test_org",
            client=httpx.Client(transport=transport),  # Pass the mocked transport
        )

        details = client._make_request(url="https://api.stellanow.com/test", method="GET")

        # Convert the dates to the expected ISO format
        created_at = datetime.fromisoformat(details["createdAt"].replace("Z", "+00:00"))
        updated_at = datetime.fromisoformat(details["updatedAt"].replace("Z", "+00:00"))

        # Assert with the correct format (including milliseconds)
        self.assertEqual(created_at.isoformat(), "2024-03-06T18:22:19.335921+00:00")
        self.assertEqual(updated_at.isoformat(), "2024-06-27T08:28:40.973269+00:00")
