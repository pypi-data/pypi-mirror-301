import unittest

from stellanow_api_internals.datatypes.workflow_mgmt import (
    StellaBaseFieldType,
    StellaEntityDetailed,
    StellaEntityField,
    StellaShortEvent,
)


class TestStellaEntityDetailedSerialization(unittest.TestCase):

    def test_stella_entity_detailed_serialization(self):
        json_data = {
            "details": {
                "projectId": "52b212f7-3da9-47eb-a2a8-adc9248dba74",
                "id": "61d16181-12f0-4f7a-a702-e0e6bb06302a",
                "name": "Metro",
                "description": "",
                "isActive": True,
                "createdAt": "2024-03-11T10:48:23.288147Z",
                "updatedAt": "2024-03-11T10:48:56.094698Z",
                "fields": [],
                "events": [
                    {"id": "e716433e-cc49-49ff-a1ba-b8a131053a12", "name": "metro_state"},
                    {"id": "1f6d835e-2f01-468f-9501-04a6f7509389", "name": "test_event_sdk"},
                ],
            },
            "status": "ok",
        }

        expected_entity = StellaEntityDetailed(
            projectId="52b212f7-3da9-47eb-a2a8-adc9248dba74",
            id="61d16181-12f0-4f7a-a702-e0e6bb06302a",
            name="Metro",
            description="",
            isActive=True,
            createdAt="2024-03-11T10:48:23.288147Z",
            updatedAt="2024-03-11T10:48:56.094698Z",
            fields=[],
            events=[
                StellaShortEvent(id="e716433e-cc49-49ff-a1ba-b8a131053a12", name="metro_state"),
                StellaShortEvent(id="1f6d835e-2f01-468f-9501-04a6f7509389", name="test_event_sdk"),
            ],
        )

        parsed_entity = StellaEntityDetailed(
            projectId=json_data["details"]["projectId"],
            id=json_data["details"]["id"],
            name=json_data["details"]["name"],
            description=json_data["details"]["description"],
            isActive=json_data["details"]["isActive"],
            createdAt=json_data["details"]["createdAt"],
            updatedAt=json_data["details"]["updatedAt"],
            fields=json_data["details"]["fields"],
            events=[StellaShortEvent(**event) for event in json_data["details"]["events"]],
        )

        self.assertEqual(parsed_entity.dict(), expected_entity.dict())

    def test_stella_entity_detailed_parsing(self):
        # Input data
        input_data = {
            "projectId": "52b212f7-3da9-47eb-a2a8-adc9248dba74",
            "id": "f4ffebe0-be4c-40ea-9e46-5fc6b7364158",
            "name": "AirQuality",
            "description": "AirQuality",
            "isActive": True,
            "createdAt": "2024-03-01T13:31:57.357604Z",
            "updatedAt": "2024-03-01T14:52:42.334055Z",
            "fields": [
                {
                    "id": "81b6d462-cac3-4fc9-89f4-20928acce88d",
                    "name": "locationId",
                    "fieldType": {"value": "Integer"},
                    "propagatedFrom": [],
                }
            ],
            "events": [
                {"id": "c36508cf-4c52-4454-81c8-1bd3981d4264", "name": "air_quality_state"},
                {"id": "1f6d835e-2f01-468f-9501-04a6f7509389", "name": "test_event_sdk"},
            ],
        }

        # Convert input data to StellaEntityDetailed instance
        entity_detailed = StellaEntityDetailed(
            id=input_data["id"],
            name=input_data["name"],
            description=input_data["description"],
            projectId=input_data["projectId"],
            isActive=input_data["isActive"],
            createdAt=input_data["createdAt"],
            updatedAt=input_data["updatedAt"],
            fields=[
                StellaEntityField(
                    id=field["id"],
                    name=field["name"],
                    fieldType=StellaBaseFieldType(**field["fieldType"]),
                    propagatedFrom=field["propagatedFrom"],
                )
                for field in input_data["fields"]
            ],
            events=[StellaShortEvent(**event) for event in input_data["events"]],
        )

        # Assertions
        self.assertEqual(entity_detailed.id, "f4ffebe0-be4c-40ea-9e46-5fc6b7364158")
        self.assertEqual(entity_detailed.name, "AirQuality")
        self.assertEqual(entity_detailed.description, "AirQuality")
        self.assertEqual(entity_detailed.projectId, "52b212f7-3da9-47eb-a2a8-adc9248dba74")
        self.assertTrue(entity_detailed.isActive)
        self.assertEqual(entity_detailed.createdAt, "2024-03-01 13:31:57")
        self.assertEqual(entity_detailed.updatedAt, "2024-03-01 14:52:42")

        self.assertEqual(len(entity_detailed.fields), 1)
        self.assertEqual(entity_detailed.fields[0].id, "81b6d462-cac3-4fc9-89f4-20928acce88d")
        self.assertEqual(entity_detailed.fields[0].name, "locationId")
        self.assertEqual(entity_detailed.fields[0].fieldType.value, "Integer")
        self.assertEqual(entity_detailed.fields[0].propagatedFrom, [])

        self.assertEqual(len(entity_detailed.events), 2)
        self.assertEqual(entity_detailed.events[0].id, "c36508cf-4c52-4454-81c8-1bd3981d4264")
        self.assertEqual(entity_detailed.events[1].id, "1f6d835e-2f01-468f-9501-04a6f7509389")
        self.assertEqual(entity_detailed.events[1].name, "test_event_sdk")
