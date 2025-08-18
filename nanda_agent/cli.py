#!/usr/bin/env python3
"""
NANDA Agent Framework - Command Line Interface
"""

def main():
    """Main CLI entry point"""
    print("NANDA Agent Framework")
    print("Create custom agents with pluggable message improvement logic")
    print()
    print("Usage:")
    print("  from nanda_agent import NANDA")
    print("  ")
    print("  def my_improvement_logic(message_text: str) -> str:")
    print("      return f'Improved: {message_text}'")
    print("  ")
    print("  nanda = NANDA(my_improvement_logic)")
    print("  nanda.start_server()")
    print()
    print("Environment Variables:")
    print("  ANTHROPIC_API_KEY    Your Anthropic API key (required)")
    print("  AGENT_ID             Custom agent ID (optional)")
    print("  PORT                 Agent bridge port (default: 6000)")

if __name__ == "__main__":
    main()