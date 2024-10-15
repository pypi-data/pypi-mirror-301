"""
Copyright (C) 2022-2024 Stella Technologies (UK) Limited.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

from uuid import uuid4

import pytest

from stellanow_api_internals.datatypes.workflow_mgmt import StellaProject, StellaWorkflowDetailed


def test_stella_project_with_none_archived():
    project = StellaProject(
        id=str(uuid4()),
        name="Test Project",
        organizationId=str(uuid4()),
        createdAt="2024-01-01T12:00:00Z",
        updatedAt="2024-01-02T12:00:00Z",
        archived=None,
    )

    assert project.archived is None
    assert project.name is "Test Project"


def test_stella_project_with_valid_archived():
    archived_date = "2024-01-03T12:00:00Z"
    project = StellaProject(
        id=str(uuid4()),
        name="Test Project",
        organizationId=str(uuid4()),
        createdAt="2024-01-01T12:00:00Z",
        updatedAt="2024-01-02T12:00:00Z",
        archived=archived_date,
    )

    assert project.archived == "2024-01-03 12:00:00"


def test_stella_project_without_archived():
    uuid = str(uuid4())
    project_dict = {
        "id": uuid,
        "name": "Test Project",
        "organizationId": uuid,
        "createdAt": "2024-01-01T12:00:00Z",
        "updatedAt": "2024-01-02T12:00:00Z",
    }
    project = StellaProject(**project_dict)

    assert project.id == uuid
    assert project.name == "Test Project"
    assert project.organizationId == uuid
    assert project.createdAt == "2024-01-01 12:00:00"
    assert project.updatedAt == "2024-01-02 12:00:00"


def test_stella_project_with_invalid_archived_format():
    with pytest.raises(ValueError):
        StellaProject(
            id=str(uuid4()),
            name="Test Project",
            organizationId=uuid4(),
            createdAt="2024-01-01T12:00:00Z",
            updatedAt="2024-01-02T12:00:00Z",
            archived="Invalid Date",
        )


def test_stella_workflow_detailed_with_none_activated_at():
    workflow = StellaWorkflowDetailed(
        id=str(uuid4()),
        name="Test Workflow",
        projectId=str(uuid4()),
        isActive=True,
        tags=["tag1", "tag2"],
        publishedVersion=1,
        createdAt="2024-01-01T12:00:00Z",
        updatedAt="2024-01-02T12:00:00Z",
        activatedAt=None,
        description="A test workflow",
        events=[],
        entities=[],
    )

    assert workflow.activatedAt is None


def test_stella_workflow_detailed_with_valid_activated_at():
    activated_at_date = "2024-01-03T12:00:00Z"
    workflow = StellaWorkflowDetailed(
        id=str(uuid4()),
        name="Test Workflow",
        projectId=str(uuid4()),
        isActive=True,
        tags=["tag1", "tag2"],
        publishedVersion=1,
        createdAt="2024-01-01T12:00:00Z",
        updatedAt="2024-01-02T12:00:00Z",
        activatedAt=activated_at_date,
        description="A test workflow",
        events=[],
        entities=[],
    )

    assert workflow.activatedAt == "2024-01-03 12:00:00"


def test_stella_workflow_detailed_with_invalid_activated_at_format():
    with pytest.raises(ValueError):
        StellaWorkflowDetailed(
            id=str(uuid4()),
            name="Test Workflow",
            projectId=str(uuid4()),
            isActive=True,
            tags=["tag1", "tag2"],
            publishedVersion=1,
            createdAt="2024-01-01T12:00:00Z",
            updatedAt="2024-01-02T12:00:00Z",
            activatedAt="Invalid Date",
            description="A test workflow",
            events=[],
            entities=[],
        )
