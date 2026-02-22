"""
Writer Agent - Produces the final polished report.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from .base import AgentMessage, BaseAgent


class WriterAgent(BaseAgent):
    """
    Final agent in the pipeline. Takes research and analysis,
    and produces a polished, reader-friendly report.
    """

    name = "Writer"
    role = "Report composition and formatting"

    def __init__(self, llm: ChatOpenAI | None = None) -> None:
        self.llm = llm or ChatOpenAI(model="gpt-4o-mini", temperature=0.4)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a Writer Agent. You receive research findings and analysis, and produce a polished, professional report.

Your responsibilities:
1. Follow the recommended structure from the Analyst
2. Write in clear, accessible language
3. Use proper formatting: headers, bullet points, short paragraphs
4. Ensure logical flow from introduction to conclusion
5. Include an executive summary at the start
6. Add a brief conclusion with key takeaways
7. Maintain accuracy - do not add information not in the research/analysis

Output format: A complete, publication-ready report with:
- Executive Summary
- Main sections (as outlined by the Analyst)
- Conclusion
- Key Takeaways""",
                ),
                ("human", "{input}"),
            ]
        )
        self.chain = self.prompt | self.llm

    def process(self, input_message: AgentMessage) -> AgentMessage:
        """Produce the final report from research and analysis."""
        analysis_content = input_message.content
        topic = input_message.metadata.get("topic", "unknown")

        # The writer receives only the analysis - the analyst has already
        # synthesized the research. In a full implementation, we might
        # pass both; here we keep the handoff clear.
        response = self.chain.invoke(
            {
                "input": f"Topic: {topic}\n\nAnalysis from Analyst Agent (use this structure and insights):\n\n{analysis_content}",
            }
        )

        return AgentMessage(
            source=self.name,
            content=response.content,
            metadata={
                "topic": topic,
                "stage": "report",
                "analysis_source": input_message.source,
            },
        )
