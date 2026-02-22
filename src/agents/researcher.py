"""
Researcher Agent - Gathers and synthesizes information on a given topic.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .base import AgentMessage, BaseAgent


class ResearcherAgent(BaseAgent):
    """
    First agent in the pipeline. Responsible for gathering factual information,
    key points, and relevant context on the user's research topic.
    """

    name = "Researcher"
    role = "Information gathering and fact synthesis"

    def __init__(self, llm: ChatOpenAI | None = None) -> None:
        self.llm = llm or ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a thorough Researcher Agent. Your job is to gather and synthesize information on the given topic.

You should:
1. Break down the topic into key subtopics
2. Identify the most important facts, figures, and context
3. Note any controversies or differing perspectives
4. Structure findings in a clear, organized manner
5. Be factual and cite logical reasoning (no external sources needed - use your knowledge)

Output format: A structured research summary with clear sections and bullet points.""",
                ),
                ("human", "{input}"),
            ]
        )
        self.chain = self.prompt | self.llm

    def process(self, input_message: AgentMessage) -> AgentMessage:
        """Gather research on the topic from the user's query."""
        topic = input_message.content
        response = self.chain.invoke({"input": f"Research topic: {topic}"})
        return AgentMessage(
            source=self.name,
            content=response.content,
            metadata={"topic": topic, "stage": "research"},
        )
