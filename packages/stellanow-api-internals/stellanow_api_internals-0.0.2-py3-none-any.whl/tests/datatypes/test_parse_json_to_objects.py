import unittest

from stellanow_api_internals.datatypes.workflow_mgmt import (
    DAGAggregationNodeData,
    DAGAwaitNodeData,
    DAGNodeEmpty,
    DAGNodeWithCondition,
    DAGNotificationNodeData,
    StellaWorkflowDAG,
    StellaWorkflowDAGEdge,
    StellaWorkflowDAGNodes,
)


class TestParseDag(unittest.TestCase):
    def test_parse_workflow_dag(self):
        config_data = {
            "id": "2afa8461-19d2-4807-a89c-87639e6d4247",
            "workflowId": "955512e1-b40d-4981-8657-df508ccc5b0e",
            "commitMessage": "",
            "versionNumber": 7,
            "isLatest": True,
            "isPublished": False,
            "createdAt": "2024-08-13T10:23:33.848233Z",
            "structure": {
                "nodes": [
                    {
                        "type": "filter",
                        "id": "c09a8800-077b-4a26-aa01-c330ace78ba0",
                        "position": {"x": 960, "y": 60},
                        "data": {
                            "displayInfo": {"title": "FilterAirState", "description": ""},
                            "config": {
                                "id": "7018fff6-114b-470e-98c2-5505eb448570",
                                "conditions": [
                                    {
                                        "id": "01c1e650-929c-4722-bbe4-f8b4e8daed0a",
                                        "left": {
                                            "id": "6a0a5f4e-6200-4ab3-b7bf-16057dd6256d",
                                            "fieldName": "eventTypeDefinitionId",
                                        },
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
                            "isStateful": False,
                        },
                    },
                    {
                        "type": "notify",
                        "id": "57b80f86-83c7-46c0-8159-8ccd0f887638",
                        "position": {"x": 960, "y": 220},
                        "data": {
                            "displayInfo": {"title": "TestDestination"},
                            "config": {
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
                            },
                            "isStateful": True,
                        },
                    },
                    {
                        "type": "propagateToSource",
                        "id": "504805b9-2cf8-4c2f-9f6c-b4469b1399ac",
                        "position": {"x": 960, "y": 380},
                        "data": {
                            "displayInfo": {"title": "Propagate to Source"},
                            "config": {"id": "5e6add30-db6a-471a-a2a1-316dc2c7a75f"},
                            "isStateful": False,
                        },
                    },
                    {
                        "type": "await",
                        "id": "await_node_123",
                        "position": {"x": 1000, "y": 400},
                        "data": {
                            "displayInfo": {"title": "Await Event", "description": "Waiting for event"},
                            "config": {
                                "id": "await_config_123",
                                "eventName": "some_event_name",
                                "waitTime": 120,
                            },
                            "isStateful": False,
                        },
                    },
                    {
                        "type": "aggregate",
                        "id": "aggregate_node_123",
                        "position": {"x": 1100, "y": 500},
                        "data": {
                            "displayInfo": {"title": "Aggregate Data"},
                            "config": {
                                "id": "aggregate_config_123",
                                "aggregated": {
                                    "id": "field_123",
                                    "fieldId": "field_456",
                                    "eventName": "event_name",
                                    "fieldName": "field_name",
                                    "multiValue": False,
                                },
                                "source": {
                                    "type": "EventType",
                                    "id": "source_123",
                                    "fieldId": "source_field_456",
                                    "multiValue": False,
                                    "eventName": "source_event",
                                    "fieldName": "source_field",
                                },
                                "interval": "1h",
                                "intervalStart": "2024-10-10T00:00:00Z",
                                "intervalLength": 60,
                            },
                            "isStateful": True,
                        },
                    },
                ],
                "edges": [
                    {
                        "id": "edge_1",
                        "source": "c09a8800-077b-4a26-aa01-c330ace78ba0",
                        "target": "57b80f86-83c7-46c0-8159-8ccd0f887638",
                    },
                    {
                        "id": "edge_2",
                        "source": "57b80f86-83c7-46c0-8159-8ccd0f887638",
                        "target": "504805b9-2cf8-4c2f-9f6c-b4469b1399ac",
                    },
                ],
            },
        }
        parsed_dag = StellaWorkflowDAG(**config_data)

        self.assertIsInstance(parsed_dag, StellaWorkflowDAG)
        self.assertEqual(len(parsed_dag.structure.nodes.root), 5)

        nodes_by_type = {node.type: node for node in parsed_dag.structure.nodes.root}

        filter_node = nodes_by_type.get("filter")
        self.assertIsNotNone(filter_node)
        self.assertEqual(filter_node.data.displayInfo.title, "FilterAirState")
        self.assertIsInstance(filter_node.data.config, DAGNodeWithCondition)

        notify_node = nodes_by_type.get("notify")
        self.assertIsNotNone(notify_node)
        self.assertEqual(notify_node.data.displayInfo.title, "TestDestination")
        self.assertIsInstance(notify_node.data.config, DAGNotificationNodeData)

        propagate_node = nodes_by_type.get("propagateToSource")
        self.assertIsNotNone(propagate_node)
        self.assertEqual(propagate_node.data.displayInfo.title, "Propagate to Source")
        self.assertIsInstance(propagate_node.data.config, DAGNodeEmpty)

        await_node = nodes_by_type.get("await")
        self.assertIsNotNone(await_node)
        self.assertEqual(await_node.data.displayInfo.title, "Await Event")
        self.assertIsInstance(await_node.data.config, DAGAwaitNodeData)

        aggregate_node = nodes_by_type.get("aggregate")
        self.assertIsNotNone(aggregate_node)
        self.assertEqual(aggregate_node.data.displayInfo.title, "Aggregate Data")
        self.assertIsInstance(aggregate_node.data.config, DAGAggregationNodeData)

        for edge in parsed_dag.structure.edges.root:
            self.assertIsInstance(edge, StellaWorkflowDAGEdge)

        self.assertEqual(parsed_dag.id, config_data["id"])
        self.assertEqual(parsed_dag.workflowId, config_data["workflowId"])
        self.assertEqual(parsed_dag.versionNumber, config_data["versionNumber"])

    def test_parse_dag_node_filter(self):
        node_data = {
            "type": "filter",
            "id": "c09a8800-077b-4a26-aa01-c330ace78ba0",
            "position": {"x": 960, "y": 60},
            "data": {
                "displayInfo": {"title": "FilterAirState", "description": ""},
                "config": {
                    "id": "7018fff6-114b-470e-98c2-5505eb448570",
                    "conditions": [
                        {
                            "id": "01c1e650-929c-4722-bbe4-f8b4e8daed0a",
                            "left": {
                                "id": "6a0a5f4e-6200-4ab3-b7bf-16057dd6256d",
                                "fieldName": "eventTypeDefinitionId",
                            },
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
                "isStateful": False,
            },
        }
        parsed_node = StellaWorkflowDAGNodes(**node_data)

        self.assertIsInstance(parsed_node, StellaWorkflowDAGNodes)
        self.assertIsInstance(parsed_node.data.config, DAGNodeWithCondition)
        self.assertEqual(parsed_node.id, node_data["id"])
        self.assertEqual(parsed_node.data.config.operator, node_data["data"]["config"]["operator"])
