# NANDA Agent Framework

A customizable improvement logic for your agents,  and easily get registered into NANDA registry

## Features

- **Pluggable Message Improvement**: Easily customize how your agents improve messages
- **Multiple AI Frameworks**: Support for LangChain, CrewAI, and custom logic
- **Agent-to-Agent Communication**: Built-in A2A communication system
- **Registry System**: Automatic agent discovery and registration
- **SSL Support**: Production-ready with Let's Encrypt certificates
- **Example Agents**: Ready-to-use examples for common use cases

## Installation

### Basic Installation

```bash
pip install nanda-agent
```

## Quick Start

### 1. Set Your API Key (For running your personal hosted agents, need API key and your own domain)

```bash
export ANTHROPIC_API_KEY="your-api-key-here"\
export DOMAIN_NAME="your-domain.com"
```

### 2. Create Your Own Agent - Development

```bash
2.1 Write your improvement logic using the framework you like. Here it is a simple moduule without any llm call. 
2.2 In the main(), create your improvement function, initialize NANDA using the improvement function, and start the server with Anthropic key and domain using nanda.start_server_api().
2.3 In the requirements.txt file add nanda-agent along with other requirements 
2.4 Move this file into your server(the domain should match to the IP address) and run this python file in background 

if langchain_pirate.py is python file name, use the below instructions to run in the background: 
nohup python3 langchain_pirate.py > out.log 2>&1 &
```


```python
#!/usr/bin/env python3
from nanda_agent import NANDA
import os

def create_custom_improvement():
    """Create your custom improvement function"""
    
    def custom_improvement_logic(message_text: str) -> str:
        """Transform messages according to your logic"""
        try:
            # Your custom transformation logic here
            improved_text = message_text.replace("hello", "greetings")
            improved_text = improved_text.replace("goodbye", "farewell")
            
            return improved_text
        except Exception as e:
            print(f"Error in improvement: {e}")
            return message_text  # Fallback to original
    
    return custom_improvement_logic

def main():
    # Create your improvement function
    my_improvement = create_custom_improvement()
    
    # Initialize NANDA with your custom logic
    nanda = NANDA(my_improvement)
    
    # Start the server
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    domain = os.getenv("DOMAIN_NAME")
    
    nanda.start_server_api(anthropic_key, domain)

if __name__ == "__main__":
    main()
```

### Using with LangChain

```python
from nanda_agent import NANDA
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_anthropic import ChatAnthropic

def create_langchain_improvement():
    llm = ChatAnthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-3-haiku-20240307"
    )
    
    prompt = PromptTemplate(
        input_variables=["message"],
        template="Make this message more professional: {message}"
    )
    
    chain = prompt | llm | StrOutputParser()
    
    def langchain_improvement(message_text: str) -> str:
        return chain.invoke({"message": message_text})
    
    return langchain_improvement

# Use it
nanda = NANDA(create_langchain_improvement())
# Start the server
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
domain = os.getenv("DOMAIN_NAME")

nanda.start_server_api(anthropic_key, domain)
```

### Using with CrewAI

```python
from nanda_agent import NANDA
from crewai import Agent, Task, Crew
from langchain_anthropic import ChatAnthropic

def create_crewai_improvement():
    llm = ChatAnthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        model="claude-3-haiku-20240307"
    )
    
    improvement_agent = Agent(
        role="Message Improver",
        goal="Improve message clarity and professionalism",
        backstory="You are an expert communicator.",
        llm=llm
    )
    
    def crewai_improvement(message_text: str) -> str:
        task = Task(
            description=f"Improve this message: {message_text}",
            agent=improvement_agent,
            expected_output="An improved version of the message"
        )
        
        crew = Crew(agents=[improvement_agent], tasks=[task])
        result = crew.kickoff()
        return str(result)
    
    return crewai_improvement

# Use it
nanda = NANDA(create_crewai_improvement())
# Start the server
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
domain = os.getenv("DOMAIN_NAME")

nanda.start_server_api(anthropic_key, domain)
```

### Checkout the examples folder for more details


## Configuration

### Environment Variables

- `ANTHROPIC_API_KEY`: Your Anthropic API key (required)
- `DOMAIN_NAME`: Domain name for SSL certificates
- `AGENT_ID`: Custom agent ID (optional, auto-generated if not provided)
- `PORT`: Agent bridge port (default: 6000)
- `IMPROVE_MESSAGES`: Enable/disable message improvement (default: true)

### Production Deployment

For production deployment with SSL:

```bash
export ANTHROPIC_API_KEY="your-api-key"
export DOMAIN_NAME="your-domain.com"
nanda-pirate
```

#### Detailed steps to be done for the deployment 
```bash
Assuming your customized improvement logic is in langchain_pirate.py


1. Copy the py and requirements file to a folder of choice in the server
cmd: scp langchain_pirate.py requirements.txt root@66.175.209.173:/opt/test-agents
For AWS Linux machines 
cmd : scp -i my-key.pem langchain_pirate.py requirements.txt ec2-user@66.175.209.173/home/ec2-user/test-agents

2. ssh into the server, ensure the latest software is in the system
cmd : ssh root@66.175.209.173
      sudo apt update  && sudo apt install python3 python3-pip python3-venv certbot

EC2 cmd : ssh ec2user@66.175.209.173
      sudo dnf update -y && sudo dnf install -y python3.11 python3.11-pip certbot

3. Move to the respective folder and create and Activate a virtual env in the folder where files are moved in step 1
cmd : cd /opt/test-agents && python3 -m venv jinoos && source jinoos/bin/activate

EC2 cmd: cd /home/ec2-user/test-agents && python3.11 -m venv jinoos && source jinoos/bin/activate

4. Download the certificates into the machine for your domain. 
(For ex: You should ensure in  DNS an A record is mapping this domain  chat1.chat39.org to IP address 66.175.209.173). Ensure the domain has to be changed
   
cmd : sudo certbot certonly --standalone -d chat1.chat39.org 

5. Copy the cert to current folder for access and provide required access
Ensure the domain has to be changed

    sudo cp -L /etc/letsencrypt/live/chat1.chat39.org/fullchain.pem .
    sudo cp -L /etc/letsencrypt/live/chat1.chat39.org/privkey.pem .
    sudo chown $USER:$USER fullchain.pem privkey.pem
    chmod 600 fullchain.pem privkey.pem


6. Install the requirements file 
cmd : python -m pip install --upgrade pip && pip3 install -r requirements.txt 

7. Ensure the env variables are available either through .env or you can provide export 
cmd : export ANTHROPIC_API_KEY=my-anthropic-key && export DOMAIN_NAME=my-domain

8. Run the new improvement logic as a batch process 
cmd : nohup python3 langchain_pirate.py > out.log 2>&1 &

9. Open the log file and you could find the agent enrollment link
cmd : cat out.log

10. Take the link and go to browser for registration

```






The framework will automatically:
- Generate SSL certificates using Let's Encrypt
- Set up proper agent registration
- Configure production-ready logging

## API Endpoints

When running with `start_server_api()`, the following endpoints are available:

- `GET /api/health` - Health check
- `POST /api/send` - Send message to agent
- `GET /api/agents/list` - List registered agents
- `POST /api/receive_message` - Receive message from agent
- `GET /api/render` - Get latest message

## Agent Communication

Agents can communicate with each other using the `@agent_id` syntax:

```
@agent123 Hello there!
```

The message will be improved using your custom logic before being sent.

## Command Line Tools

```bash
# Show help
nanda-agent --help

# List available examples
nanda-agent --list-examples

# Run specific examples
nanda-pirate              # Simple pirate agent
nanda-pirate-langchain    # LangChain pirate agent
nanda-sarcastic           # CrewAI sarcastic agent
```

## Architecture

The NANDA framework consists of:

1. **AgentBridge**: Core communication handler
2. **Message Improvement System**: Pluggable improvement logic
3. **Registry System**: Agent discovery and registration
4. **A2A Communication**: Agent-to-agent messaging
5. **Flask API**: External communication interface

## Development

### Creating Custom Agents

1. Create your improvement function
2. Initialize NANDA with your function
3. Start the server
4. Your agent is ready to communicate!

## Examples

The framework includes several example agents:

- **Simple Pirate Agent**: Basic string replacement
- **LangChain Pirate Agent**: AI-powered pirate transformation
- **CrewAI Sarcastic Agent**: Team-based sarcastic responses

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please see CONTRIBUTING.md for guidelines.

## Support

For issues and questions:
- GitHub Issues: https://github.com/nanda-ai/nanda-agent/issues
- Email: support@nanda.ai

## Changelog

### v1.0.0
- Initial release
- Basic NANDA framework
- LangChain integration
- CrewAI integration
- Example agents
- Production deployment support