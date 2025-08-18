#!/usr/bin/env python3
"""
NANDA Agent Framework - Customizable AI Agent Communication System

This package provides a framework for creating customizable AI agents with pluggable
message improvement logic, built on top of the python_a2a communication framework.
"""

from .core.nanda import NANDA
from .core.agent_bridge import (
    AgentBridge, 
    message_improver, 
    register_message_improver, 
    get_message_improver, 
    list_message_improvers
)

__version__ = "1.0.0"
__author__ = "NANDA Team"
__email__ = "support@nanda.ai"

# Export main classes and functions
__all__ = [
    "NANDA",
    "AgentBridge",
    "message_improver",
    "register_message_improver", 
    "get_message_improver",
    "list_message_improvers"
]