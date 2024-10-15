import json
import unittest
from json import loads

from stellanow_api_internals.datatypes.workflow_mgmt import (
    DAGNodeConfig,
    DAGNodeEventTypeFieldDefinition,
    DAGNotificationField,
    DAGNotificationNodeData,
)


class TestDAGNodeConfigSerialization(unittest.TestCase):

    def test_dag_node_config_serialization(self):
        # Create a sample DAGNotificationNodeData object
        notification_data = DAGNotificationNodeData(
            id="32c54d47-ded2-4785-aadd-7ab13cc0c116",
            channel="5d50656f-e5c7-4464-84b5-86f283e59bf2",
            fields=[
                DAGNotificationField(
                    targetFieldName="name",
                    source=DAGNodeEventTypeFieldDefinition(
                        id="db096e59-cf14-43fb-bdeb-43a1cc5fe497",
                        type="EventType",
                        fieldId="1a9b7af0-3e8d-4144-8c71-71eb2505d140",
                        eventName="air_quality_state",
                        fieldName="ijp.name",
                        multiValue=False,
                    ),
                )
            ],
        )

        config_dict = DAGNodeConfig(
            id="32c54d47-ded2-4785-aadd-7ab13cc0c116", notificationData=notification_data.model_dump()
        ).to_dict()

        expected_dict = {
            "id": "32c54d47-ded2-4785-aadd-7ab13cc0c116",
            "channel": "5d50656f-e5c7-4464-84b5-86f283e59bf2",
            "fields": [
                {
                    "targetFieldName": "name",
                    "source": {
                        "type": "EventType",
                        "id": "db096e59-cf14-43fb-bdeb-43a1cc5fe497",
                        "fieldId": "1a9b7af0-3e8d-4144-8c71-71eb2505d140",
                        "multiValue": False,
                        "eventName": "air_quality_state",
                        "fieldName": "ijp.name",
                    },
                }
            ],
        }

        self.assertEqual(config_dict, expected_dict)

        config_json = json.dumps(config_dict, indent=4)
        expected_json = json.dumps(expected_dict, indent=4)

        self.assertEqual(config_json, expected_json)

    def test_parse_dag_node_config(self):
        # Simulating a JSON payload from the system
        config_data = {
            "id": "7018fff6-114b-470e-98c2-5505eb448570",
            "filterData": {
                "id": "7018fff6-114b-470e-98c2-5505eb448570",
                "conditions": [
                    {
                        "id": "01c1e650-929c-4722-bbe4-f8b4e8daed0a",
                        "left": {"id": "6a0a5f4e-6200-4ab3-b7bf-16057dd6256d", "fieldName": "eventTypeDefinitionId"},
                        "right": {
                            "type": "ExplicitType",
                            "id": "0bd4120b-8940-4ce3-bee3-4d8de39a9e40",
                            "value": "air_quality_state",
                            "multiValue": False,
                        },
                        "condition": "EQ",
                        "negate": False,
                        "fieldType": {"value": "String"},
                    }
                ],
                "operator": "AND",
            },
        }

        # Parse the config and flatten the fields
        config_dict = DAGNodeConfig(id=config_data["id"], filterData=config_data["filterData"]).to_dict()

        # Ensure the JSON output is flattened correctly
        expected_dict = {
            "id": "7018fff6-114b-470e-98c2-5505eb448570",
            "conditions": [
                {
                    "id": "01c1e650-929c-4722-bbe4-f8b4e8daed0a",
                    "left": {"id": "6a0a5f4e-6200-4ab3-b7bf-16057dd6256d", "fieldName": "eventTypeDefinitionId"},
                    "right": {
                        "type": "ExplicitType",
                        "id": "0bd4120b-8940-4ce3-bee3-4d8de39a9e40",
                        "value": "air_quality_state",
                        "multiValue": False,
                    },
                    "condition": "EQ",
                    "negate": False,
                    "fieldType": {"value": "String"},
                }
            ],
            "operator": "AND",
        }

        self.assertEqual(config_dict, expected_dict)

        config_json = json.dumps(config_dict, indent=4)
        expected_json = json.dumps(expected_dict, indent=4)

        self.assertEqual(loads(expected_json), loads(config_json))
