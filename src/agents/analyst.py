"""
Analyst Agent - Analyzes research and extracts key insights.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .base import AgentMessage, BaseAgent


class AnalystAgent(BaseAgent):
    """
    Second agent in the pipeline. Receives research from the Researcher,
    analyzes it, and produces structured insights for the Writer.
    """

    name = "Analyst"
    role = "Critical analysis and insight extraction"

    def __init__(self, llm: ChatOpenAI | None = None) -> None:
        self.llm = llm or ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an Analyst Agent. You receive research findings and transform them into actionable insights.

Your responsibilities:
1. Critique and validate the research - identify gaps or strong points
2. Extract key takeaways and implications
3. Prioritize information by importance and relevance
4. Identify connections between different pieces of information
5. Suggest the logical structure for presenting findings (outline)
6. Note any caveats or limitations

Output format: Structured analysis with:
- Key Insights (prioritized list)
- Implications
- Recommended Report Structure (outline)
- Caveats/Limitations""",
                ),
                ("human", "{input}"),
            ]
        )
        self.chain = self.prompt | self.llm

    def process(self, input_message: AgentMessage) -> AgentMessage:
        """Analyze research and produce insights."""
        research_content = input_message.content
        topic = input_message.metadata.get("topic", "unknown")

        response = self.chain.invoke(
            {
                "input": f"Topic: {topic}\n\nResearch from Researcher Agent:\n\n{research_content}",
            }
        )

        return AgentMessage(
            source=self.name,
            content=response.content,
            metadata={
                "topic": topic,
                "stage": "analysis",
                "research_source": input_message.source,
            },
        )
