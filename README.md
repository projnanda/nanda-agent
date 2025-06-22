# Internet of Agents

A distributed agent system that enables multiple agents to run and communicate with each other over HTTP/HTTPS.

## Overview

This system allows you to run multiple agents with unique IDs, each operating on different ports for bridge and API communication. The agents can communicate with each other and with external services through a registry.

## Prerequisites

- Python 3.x
- Bash shell
- Internet connectivity
- Anthropic API key
- Let's Encrypt SSL certificates
- Virtual environment (venv)

## Configuration

The system requires a configuration file at `/etc/internet_of_agents.env` with the following environment variables:

```bash
# Required environment variables
ANTHROPIC_API_KEY="your-api-key-here"
AGENT_ID_PREFIX="your-prefix"
DOMAIN_NAME="your-domain.com"
REGISTRY_URL="https://your-registry-url:port"

# Optional environment variables
NUM_AGENTS=1  # Defaults to 1 if not specified
```

## Agent Configuration

The agent system can be configured through the following parameters in `start_running_agents.sh`:

```bash
# Starting port numbers for bridge and API
START_BRIDGE_PORT=6000
START_API_PORT=6001
```

### Port Configuration
- Bridge ports start from `START_BRIDGE_PORT` and increment by 2
- API ports start from `START_API_PORT` and increment by 2
- For example, with NUM_AGENTS=3:
  - Bridge ports: 6000, 6002, 6004
  - API ports: 6001, 6003, 6005

### Agent IDs
- Agent IDs follow different patterns based on the domain:
  - For nanda-registry.com domains: `agentm{AGENT_ID_PREFIX}{INDEX}`
  - For other domains: `agents{AGENT_ID_PREFIX}{INDEX}`
- Example with AGENT_ID_PREFIX=6 and NUM_AGENTS=3:
  - For nanda-registry.com: agentm60, agentm61, agentm62
  - For other domains: agents60, agents61, agents62

## Usage

1. Set up the environment file:
   ```bash
   sudo nano /etc/internet_of_agents.env
   # Add the required environment variables
   ```

2. Ensure SSL certificates are in place:
- Certificate: `~/.local/ssl/fullchain.pem`
- Private key: `~/.local/ssl/privkey.pem`
- CSR (temporary): `~/.local/ssl/cert.csr`

3. Make the script executable:
   ```bash
   chmod +x start_running_agents.sh
   ```

4. Run the script:
   ```bash
   ./start_running_agents.sh
   ```

## Monitoring and Management

### Check Running Agents
```bash
ps aux | grep run_ui_agent_https
```

### Stop All Agents
```bash
for pid in logs/*.pid; do kill $(cat $pid); done
```

### Logs
- Agent logs are stored in the `logs` directory
- Each agent has its own log file: `logs/agentm{ID}_logs.txt`
- Process IDs are stored in: `logs/agentm{ID}.pid`

## Network Configuration

The system automatically detects the server's IP address using:
1. AWS checkip service
2. ifconfig.me service
3. Falls back to localhost.com if both fail

Each agent is configured with:
- Public URL: `http://{SERVER_IP}:{BRIDGE_PORT}`
- API URL: `https://{DOMAIN_NAME}:{API_PORT}`

## Registry

Agents are registered with a central registry specified by the REGISTRY_URL environment variable.
The registry URL should be a valid HTTPS endpoint.

## Security

- API communication is secured using SSL certificates from Let's Encrypt
- Environment variables are stored in a system-wide configuration file
- Each agent runs in its own process
- Virtual environment isolation

## Troubleshooting

1. If agents fail to start:
   - Check if ports are available
   - Verify environment variables in `/etc/internet_of_agents.env`
   - Check SSL certificate paths
   - Check logs in the `logs` directory

2. If agents can't communicate:
   - Verify network connectivity
   - Check if registry is accessible
   - Ensure ports are not blocked by firewall
   - Verify SSL certificate validity

## License

MIT License

Copyright (c) 2024 Internet of Agents

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE. 