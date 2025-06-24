#!/usr/bin/env python3
"""
Sarcastic CrewAI Agent
- Uses CrewAI to improve messages to be sarcastic
- Uses NANDA to create agent_bridge server with sarcastic improvement
"""

import os
from crewai import Agent, Task, Crew
from langchain_anthropic import ChatAnthropic
from nanda import NANDA

# Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

def create_sarcastic_improvement():
    """Create CrewAI-based sarcastic improvement function"""
    
    # Check API key
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    
    # Setup LLM for CrewAI
    llm = ChatAnthropic(
        api_key=ANTHROPIC_API_KEY,
        model="claude-3-haiku-20240307",
        temperature=0.9,
        max_tokens=300
    )
    
    # Create CrewAI Agent for sarcastic messaging
    sarcastic_agent = Agent(
        role="Sarcastic Message Transformer",
        goal="Transform regular messages into witty, sarcastic versions",
        backstory="""You are a witty, sarcastic communicator who loves to add clever irony and humor to messages. 
        You transform regular messages into sarcastic versions while keeping the core meaning intact.
        You're clever with words and enjoy subtle mockery and dry humor.""",
        llm=llm,
        verbose=False
    )
    
    def sarcastic_improvement_logic(message_text: str) -> str:
        """CrewAI function to improve message to be sarcastic"""
        try:
            print(f"😏 Making message sarcastic: {message_text[:50]}...")
            
            # Create task for the agent
            sarcastic_task = Task(
                description=f"""Transform this regular message into a sarcastic, witty version:
                
Original message: "{message_text}"

Make it sarcastic but keep the same meaning. Use irony, dry humor, and wit. 
Add subtle mockery while still being clever and funny.
Don't be mean, just witty and sarcastic.
Return only the sarcastic version, no explanations.""",
                agent=sarcastic_agent,
                expected_output="A sarcastic, witty version of the original message"
            )
            
            # Create crew and execute
            crew = Crew(
                agents=[sarcastic_agent],
                tasks=[sarcastic_task],
                verbose=False
            )
            
            result = crew.kickoff()
            sarcastic_msg = str(result).strip()
            
            print(f"😏 Sarcastic result: {sarcastic_msg[:50]}...")
            return sarcastic_msg
            
        except Exception as e:
            print(f"❌ CrewAI error: {e}")
            # Simple fallback
            return f"Oh wow, {message_text.lower()}... how absolutely thrilling! 🙄"
    
    return sarcastic_improvement_logic

if __name__ == "__main__":
    try:
        print("😏 Creating CrewAI sarcastic improvement logic...")
        
        # Create the sarcastic improvement function
        my_improvement_logic = create_sarcastic_improvement()
        
        print("🤖 Initializing NANDA with sarcastic improvement...")
        
        # Create NANDA with the sarcastic improvement logic
        nanda = NANDA(my_improvement_logic)
        
        print("🚀 Starting agent_bridge server with sarcastic CrewAI improvement...")
        
        # Start the server
        nanda.start_server()
        
    except ValueError as e:
        print(f"❌ {e}")
        print("🔧 Set ANTHROPIC_API_KEY environment variable")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc() 