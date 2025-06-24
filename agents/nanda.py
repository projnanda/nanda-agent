#!/usr/bin/env python3
"""
NANDA - Custom Message Improvement for Agent Bridge
- Accepts any custom improvement logic function
- Creates agent_bridge server with custom improve_message_direct
"""

import os
import sys

# Handle different import contexts
try:
    from agent_bridge import *
except ModuleNotFoundError:
    # If running from parent directory, add current directory to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    from agent_bridge import *

class NANDA:
    """NANDA class to create agent_bridge with custom improvement logic"""
    
    def __init__(self, improvement_logic):
        """
        Initialize NANDA with custom improvement logic
        
        Args:
            improvement_logic: Function that takes (message_text: str) -> str
        """
        self.improvement_logic = improvement_logic
        self.bridge = None
        print(f"🤖 NANDA initialized with custom improvement logic: {improvement_logic.__name__}")
        
        # Register the custom improvement logic
        self.register_custom_improver()
        
        # Create agent bridge with custom logic
        self.create_agent_bridge()
    
    def register_custom_improver(self):
        """Register the custom improvement logic with agent_bridge"""
        register_message_improver("nanda_custom", self.improvement_logic)
        print(f"🔧 Custom improvement logic '{self.improvement_logic.__name__}' registered")
    
    def create_agent_bridge(self):
        """Create AgentBridge with custom improvement logic"""
        # Create standard AgentBridge
        self.bridge = AgentBridge()
        
        # Set custom improver as active (replaces improve_message_direct)
        self.bridge.set_message_improver("nanda_custom")
        print(f"✅ AgentBridge created with custom improve_message_direct: {self.improvement_logic.__name__}")
    
    def start_server(self):
        """Start the agent_bridge server with custom improvement logic"""
        print("🚀 NANDA starting agent_bridge server with custom logic...")
        
        # Register with the registry if PUBLIC_URL is set
        public_url = os.getenv("PUBLIC_URL")
        api_url = os.getenv("API_URL")
        if public_url:
            register_with_registry(AGENT_ID, public_url, api_url)
        else:
            print("WARNING: PUBLIC_URL environment variable not set. Agent will not be registered.")
        

        # Start the server
        IMPROVE_MESSAGES = os.getenv("IMPROVE_MESSAGES", "true").lower() in ("true", "1", "yes", "y")
        
        print(f"\n🚀 Starting Agent {AGENT_ID} bridge on port {PORT}")
        print(f"Agent terminal port: {TERMINAL_PORT}")
        print(f"Message improvement feature is {'ENABLED' if IMPROVE_MESSAGES else 'DISABLED'}")
        print(f"Logging conversations to {os.path.abspath(LOG_DIR)}")
        print(f"🔧 Using custom improvement logic: {self.improvement_logic.__name__}")
        
        # Run the agent bridge server
        run_server(self.bridge, host="0.0.0.0", port=PORT) 