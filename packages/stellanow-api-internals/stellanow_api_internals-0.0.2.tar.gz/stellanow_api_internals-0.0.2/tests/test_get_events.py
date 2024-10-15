from stellanow_api_internals.datatypes.workflow_mgmt import StellaEventDetailed

MOCK_RESPONSE_PAGE_1 = {
    "details": {
        "pageNumber": 1,
        "numberOfPages": 2,
        "pageSize": 1,
        "total": 2,
        "results": [
            {
                "id": "173fbe3d-04a4-47a1-a038-83262aa56a70",
                "projectId": "52b212f7-3da9-47eb-a2a8-adc9248dba74",
                "name": "electric_state_frequency",
                "isActive": True,
                "createdAt": "2024-03-06T18:22:19.335921Z",
                "updatedAt": "2024-06-27T08:28:40.973269Z",
            },
        ],
    },
    "status": "ok",
}

MOCK_RESPONSE_PAGE_2 = {
    "details": {
        "pageNumber": 2,
        "numberOfPages": 2,
        "pageSize": 1,
        "total": 2,
        "results": [
            {
                "id": "1f6d835e-2f01-468f-9501-04a6f7509389",
                "projectId": "52b212f7-3da9-47eb-a2a8-adc9248dba74",
                "name": "test_event_sdk",
                "isActive": True,
                "createdAt": "2024-04-09T11:51:55.966189Z",
                "updatedAt": "2024-07-22T15:51:32.276369Z",
            },
        ],
    },
    "status": "ok",
}

MOCK_EVENT_RESPONSE = {
    "details": {
        "id": "173fbe3d-04a4-47a1-a038-83262aa56a70",
        "name": "Test Event",
        "description": "Test event description",
        "projectId": "52b212f7-3da9-47eb-a2a8-adc9248dba74",
        "isActive": True,
        "createdAt": "2024-03-06T18:22:19.335921Z",
        "updatedAt": "2024-06-27T08:28:40.973269Z",
        "entities": [{"id": "entity1", "name": "Entity 1"}, {"id": "entity2", "name": "Entity 2"}],
        "fields": [
            {"id": "field1", "name": "Field 1", "fieldType": {"value": "string"}, "required": True},
            {"id": "field2", "name": "Field 2", "fieldType": {"value": "int"}, "required": False},
        ],
    },
    "status": "ok",
}


def test_get_event_details(mock_workflow_client):
    workflow_client = mock_workflow_client(MOCK_EVENT_RESPONSE)

    event_details: StellaEventDetailed = workflow_client.get_event_details(
        event_id="173fbe3d-04a4-47a1-a038-83262aa56a70"
    )

    assert event_details.id == "173fbe3d-04a4-47a1-a038-83262aa56a70"
    assert event_details.name == "Test Event", "Event name mismatch"
    assert event_details.description == "Test event description", "Event description mismatch"
    assert event_details.projectId == "52b212f7-3da9-47eb-a2a8-adc9248dba74", "Project ID mismatch"
    assert event_details.isActive is True, "isActive value mismatch"

    assert event_details.createdAt == "2024-03-06 18:22:19", "createdAt mismatch"
    assert event_details.updatedAt == "2024-06-27 08:28:40", "updatedAt mismatch"

    assert len(event_details.entities) == 2, "Entities count mismatch"
    assert event_details.entities[0].id == "entity1", "Entity 1 ID mismatch"
    assert event_details.entities[0].name == "Entity 1", "Entity 1 name mismatch"
    assert event_details.entities[1].id == "entity2", "Entity 2 ID mismatch"
    assert event_details.entities[1].name == "Entity 2", "Entity 2 name mismatch"

    assert len(event_details.fields) == 2, "Fields count mismatch"
    assert event_details.fields[0].id == "field1", "Field 1 ID mismatch"
    assert event_details.fields[0].name == "Field 1", "Field 1 name mismatch"
    assert event_details.fields[0].fieldType.value == "string", "Field 1 type mismatch"
    assert event_details.fields[0].required is True, "Field 1 required value mismatch"

    assert event_details.fields[1].id == "field2", "Field 2 ID mismatch"
    assert event_details.fields[1].name == "Field 2", "Field 2 name mismatch"
    assert event_details.fields[1].fieldType.value == "int", "Field 2 type mismatch"
    assert event_details.fields[1].required is False, "Field 2 required value mismatch"
