# Multi-Agent Research Pipeline

A collaborative multi-agent system built with **LangChain** that demonstrates agents working together to solve a real-world problem: **research and report generation**.

## Problem Statement

Generating high-quality research reports typically requires distinct skills: gathering information, analyzing it critically, and composing a polished document. A single LLM can attempt all three, but **specialized agents** with clear roles produce better, more structured output. This project implements that division of labor.

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   User      │     │ Researcher  │     │   Analyst   │
│   Topic     │────▶│   Agent     │────▶│   Agent     │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                                               ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Final     │     │   Writer    │     │  Insights   │
│   Report    │◀────│   Agent     │◀────│  + Outline  │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Agent Roles

| Agent | Responsibility | Input | Output |
|-------|----------------|-------|--------|
| **Researcher** | Gather facts, break down topic, identify key points | User topic | Structured research summary |
| **Analyst** | Critique research, extract insights, propose structure | Research summary | Key insights + report outline |
| **Writer** | Compose polished report following structure | Analysis + outline | Final report |

### Design Decisions

1. **Sequential Pipeline**: Each agent depends on the previous. No parallelization—handoffs are explicit and the flow is easy to reason about.

2. **Structured Handoffs**: `AgentMessage` carries both content and metadata (e.g., topic) so context flows through the pipeline.

3. **Shared LLM Instance**: All agents use the same `ChatOpenAI` instance for consistency and easy configuration.

4. **Extensibility**: Adding a new agent (e.g., Fact-Checker, SEO Optimizer) means implementing `BaseAgent` and appending to the pipeline list.

## Running Tests

```bash
python -m unittest discover tests -v
```

## Project Structure

```
multi-agent-research/
├── main.py                 # Entry point
├── requirements.txt
├── .env.example
├── README.md
├── tests/
│   └── test_pipeline.py    # Unit tests
└── src/
    ├── config.py           # Environment configuration
    ├── agents/
    │   ├── base.py         # BaseAgent, AgentMessage
    │   ├── researcher.py   # ResearcherAgent
    │   ├── analyst.py      # AnalystAgent
    │   └── writer.py       # WriterAgent
    └── orchestration/
        └── pipeline.py     # ResearchPipeline
```

## Setup

### 1. Clone and install

```bash
git clone <repository-url>
cd multi-agent-research
pip install -r requirements.txt
```

### 2. Configure API key

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key:
# OPENAI_API_KEY=sk-your-key-here
```

### 3. Run

```bash
# With topic as argument
python main.py "Impact of AI on software development"

# Interactive mode (prompts for topic)
python main.py
```

## Example Output

For topic *"Key challenges in adopting microservices"*:

1. **Researcher** produces a summary of challenges (complexity, data consistency, testing, etc.)
2. **Analyst** extracts insights, prioritizes them, and suggests a report structure
3. **Writer** produces a full report with executive summary, sections, and conclusion

## Framework Choice: LangChain

- **Widely adopted** in production LLM applications
- **Prompt templates** and chains keep agent logic clean
- **Easy model swapping** (OpenAI, Anthropic, local) via unified interface
- **Composable**—agents can be extended with tools (e.g., web search, code execution) later

## Future Extensions

- **Tools**: Researcher could use `TavilySearchResults` or similar for web search
- **Human-in-the-loop**: Analyst output could be reviewed before writing
- **Parallel branches**: Separate agents for technical vs. business audiences
- **Streaming**: Stream Writer output for long reports

## License

MIT
