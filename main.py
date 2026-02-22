#!/usr/bin/env python3
"""
Multi-Agent Research Pipeline - Entry Point

Usage:
    python main.py "Your research topic here"
    python main.py  # Interactive mode

Example:
    python main.py "Impact of AI on software development in 2024"
"""

import sys

from src.orchestration import ResearchPipeline


def main() -> None:
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("Enter research topic: ").strip() or "Emerging trends in artificial intelligence"

    print(f"\n🔬 Research Pipeline starting for: {topic}\n")
    print("-" * 60)

    pipeline = ResearchPipeline()
    result = pipeline.run(topic)

    if not result.success:
        print(f"\n❌ Error: {result.error}")
        sys.exit(1)

    print("\n📋 Pipeline Stages (preview):")
    for i, stage in enumerate(result.stages, 1):
        print(f"\n  {i}. {stage['agent']}:")
        print(f"     {stage['output_preview']}")

    print("\n" + "=" * 60)
    print("📄 FINAL REPORT")
    print("=" * 60)
    print(result.report)
    print("\n" + "=" * 60)
    print("✅ Pipeline complete.")


if __name__ == "__main__":
    main()
