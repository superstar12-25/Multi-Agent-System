"""
Research Pipeline - Orchestrates the multi-agent workflow.

Architecture:
    User Topic → Researcher → Analyst → Writer → Final Report

Each agent receives output from the previous agent and produces
input for the next. Metadata (e.g., topic) flows through the pipeline.
"""

from dataclasses import dataclass, field

from langchain_openai import ChatOpenAI

from ..agents import AnalystAgent, ResearcherAgent, WriterAgent
from ..agents.base import AgentMessage
from ..config import LLM_MODEL, validate_config


@dataclass
class PipelineResult:
    """Result of a full pipeline run."""

    topic: str
    report: str
    stages: list[dict[str, str]] = field(default_factory=list)
    success: bool = True
    error: str | None = None


class ResearchPipeline:
    """
    Orchestrates the sequential flow: Researcher → Analyst → Writer.

    Design decisions:
    - Sequential flow: Each agent depends on the previous (no parallel branches)
    - Shared LLM: Agents share a single LLM instance (configurable)
    - Metadata passing: Topic and stage info flows through for context
    - Extensible: New agents can be inserted by modifying the pipeline list
    """

    def __init__(self, llm: ChatOpenAI | None = None) -> None:
        self.llm = llm or ChatOpenAI(model=LLM_MODEL, temperature=0.3)
        self.researcher = ResearcherAgent(llm=self.llm)
        self.analyst = AnalystAgent(llm=self.llm)
        self.writer = WriterAgent(llm=self.llm)
        self._agents = [self.researcher, self.analyst, self.writer]

    def run(self, topic: str) -> PipelineResult:
        """
        Execute the full pipeline: research → analysis → report.

        Returns:
            PipelineResult with the final report and intermediate stages.
        """
        if not validate_config():
            return PipelineResult(
                topic=topic,
                report="",
                success=False,
                error="OPENAI_API_KEY not set. Copy .env.example to .env and add your API key.",
            )

        stages: list[dict[str, str]] = []
        current_message = AgentMessage(source="user", content=topic)

        try:
            for agent in self._agents:
                current_message = agent.process(current_message)
                stages.append(
                    {
                        "agent": agent.name,
                        "output_preview": current_message.content[:200] + "..."
                        if len(current_message.content) > 200
                        else current_message.content,
                    }
                )

            return PipelineResult(
                topic=topic,
                report=current_message.content,
                stages=stages,
                success=True,
            )

        except Exception as e:
            return PipelineResult(
                topic=topic,
                report=current_message.content if current_message else "",
                stages=stages,
                success=False,
                error=str(e),
            )
