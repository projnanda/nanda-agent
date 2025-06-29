#!/usr/bin/env python3
"""
Pirate LangChain Agent
- Uses LangChain to improve messages to English pirate
- Uses NANDA to create agent_bridge server with pirate improvement
"""

import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_anthropic import ChatAnthropic
from nanda import NANDA

# Configuration
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
DOMAIN_NAME = os.getenv("DOMAIN_NAME", "localhost")

def create_pirate_improvement():
    """Create LangChain-based pirate improvement function"""
    
    # Check API key
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    
    # Setup LangChain LLM
    llm = ChatAnthropic(
        api_key=ANTHROPIC_API_KEY,
        model="claude-3-haiku-20240307",
        temperature=0.7,
        max_tokens=300
    )
    
    # Create pirate prompt template
    prompt = PromptTemplate(
        input_variables=["message"],
        template="""Convert this message to authentic pirate English while keeping the original meaning and intent.

Guidelines:
- Use pirate vocabulary (ahoy, matey, ye, yer, savvy, etc.)
- Replace "you" with "ye" or "yer"
- Replace "my" with "me"
- Keep the core message intact
- Don't make it too theatrical

Message: {message}

Pirate version:"""
    )
    
    # Create LangChain chain
    chain = prompt | llm | StrOutputParser()
    
    def pirate_improvement_logic(message_text: str) -> str:
        """LangChain function to improve message to English pirate"""
        try:
            print(f"🏴‍☠️ Converting to pirate: {message_text[:50]}...")
            result = chain.invoke({"message": message_text})
            pirate_msg = result.strip()
            print(f"🏴‍☠️ Pirate result: {pirate_msg[:50]}...")
            return pirate_msg
        except Exception as e:
            print(f"❌ LangChain error: {e}")
            # Simple fallback
            return f"Ahoy! {message_text}, matey!"
    
    return pirate_improvement_logic

if __name__ == "__main__":
    try:
        print("🏴‍☠️ Creating LangChain pirate improvement logic...")
        
        # Create the pirate improvement function
        my_improvement_logic = create_pirate_improvement()
        
        print("🤖 Initializing NANDA with pirate improvement...")
        
        # Create NANDA with the pirate improvement logic
        nanda = NANDA(my_improvement_logic)
        
        print("🚀 Starting agent_bridge server with pirate LangChain improvement...")
        
        # Start the server
        # nanda.start_server()
        nanda.start_server_api(ANTHROPIC_API_KEY, DOMAIN_NAME)
        
    except ValueError as e:
        print(f"❌ {e}")
        print("🔧 Set ANTHROPIC_API_KEY environment variable")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc() 