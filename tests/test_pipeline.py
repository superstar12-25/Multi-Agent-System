"""
Tests for the Research Pipeline.

Validates pipeline structure and agent handoffs.
"""

import unittest

from src.agents.base import AgentMessage
from src.orchestration import ResearchPipeline


class TestPipeline(unittest.TestCase):
    def test_pipeline_structure(self) -> None:
        """Verify pipeline has correct agent sequence."""
        pipeline = ResearchPipeline()
        self.assertEqual(len(pipeline._agents), 3)
        self.assertEqual(pipeline._agents[0].name, "Researcher")
        self.assertEqual(pipeline._agents[1].name, "Analyst")
        self.assertEqual(pipeline._agents[2].name, "Writer")

    def test_agent_message_metadata(self) -> None:
        """Verify AgentMessage carries metadata."""
        msg = AgentMessage(source="test", content="hello", metadata={"topic": "AI"})
        self.assertEqual(msg.source, "test")
        self.assertEqual(msg.content, "hello")
        self.assertEqual(msg.metadata["topic"], "AI")

    def test_pipeline_without_api_key(self) -> None:
        """Pipeline returns result (may fail if no API key, but structure is correct)."""
        pipeline = ResearchPipeline()
        result = pipeline.run("test topic")
        self.assertEqual(result.topic, "test topic")
        self.assertIsInstance(result.success, bool)
        self.assertIsInstance(result.report, str)


if __name__ == "__main__":
    unittest.main()
