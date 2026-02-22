"""
Base agent abstraction - Shared interface for all pipeline agents.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class AgentMessage:
    """Structured message passed between agents."""

    source: str
    content: str
    metadata: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}


class BaseAgent(ABC):
    """Abstract base for all pipeline agents."""

    name: str
    role: str

    @abstractmethod
    def process(self, input_message: AgentMessage) -> AgentMessage:
        """Process incoming message and return output for next agent."""
        pass
