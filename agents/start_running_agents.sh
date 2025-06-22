#!/bin/bash
source /opt/internet_of_agents/venv/bin/activate

# Source the environment file
if [ -f "/etc/internet_of_agents.env" ]; then
    source /etc/internet_of_agents.env
else
    echo "Error: /etc/internet_of_agents.env not found"
    exit 1
fi

# Configuration
START_BRIDGE_PORT=6000
START_API_PORT=6001

# Check for required environment variables
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "Error: ANTHROPIC_API_KEY not found in environment file"
    exit 1
fi

if [ -z "$AGENT_ID_PREFIX" ]; then
    echo "Error: AGENT_ID_PREFIX not found in environment file"
    exit 1
fi

if [ -z "$DOMAIN_NAME" ]; then
    echo "Error: DOMAIN_NAME not found in environment file"
    exit 1
fi

if [ -z "$REGISTRY_URL" ]; then
    echo "Error: REGISTRY_URL not found in environment file"
    exit 1
fi

# Use NUM_AGENTS from environment or default to 1
NUM_AGENTS=${NUM_AGENTS:-1}
echo "Using NUM_AGENTS=$NUM_AGENTS"
echo "Using AGENT_ID_PREFIX=$AGENT_ID_PREFIX"
echo "Using DOMAIN_NAME=$DOMAIN_NAME"
echo "Using REGISTRY_URL=$REGISTRY_URL"

# SSL Configuration
CERT_PATH="$HOME/.local/ssl/fullchain.pem"  # Path to SSL certificate
KEY_PATH="$HOME/.local/ssl/privkey.pem"     # Path to SSL private key

# Create logs directory if it doesn't exist
mkdir -p logs



# Generate the list of ports
BRIDGE_PORTS=()
API_PORTS=()
for ((i=0; i<NUM_AGENTS; i++)); do
    BRIDGE_PORTS+=($((START_BRIDGE_PORT + i*2)))
    API_PORTS+=($((START_API_PORT + i*2)))
done

# Get the server IP address (assumes a public IP)
SERVER_IP=$(curl -s http://checkip.amazonaws.com)

# If the above command fails, try another method
if [ -z "$SERVER_IP" ]; then
    SERVER_IP=$(curl -s ifconfig.me)
fi

# If both methods fail, use localhost
if [ -z "$SERVER_IP" ]; then
    SERVER_IP="localhost.com"
    echo "Could not determine IP automatically, using default: $SERVER_IP"
else
    echo "Detected server IP: $SERVER_IP"
fi

# Start each agent
for i in "${!BRIDGE_PORTS[@]}"; do
    if [[ "$DOMAIN_NAME" == *"nanda-registry.com"* ]]; then
        AGENT_ID="agentm${AGENT_ID_PREFIX}$((i))"
    else
        AGENT_ID="agents${AGENT_ID_PREFIX}$((i))"
    fi
    BRIDGE_PORT=${BRIDGE_PORTS[$i]}
    API_PORT=${API_PORTS[$i]}
    PUBLIC_URL="http://$SERVER_IP:$BRIDGE_PORT"
    API_URL="https://${DOMAIN_NAME}:$API_PORT"
    
    echo "Starting $AGENT_ID on bridge port $BRIDGE_PORT and API port $API_PORT"
    echo "Public URL: $PUBLIC_URL"
    echo "API URL: $API_URL"
    
    PYTHONUNBUFFERED=1
    nohup python3 -u run_ui_agent_https.py --id "$AGENT_ID" --port "$BRIDGE_PORT" --api-port "$API_PORT" --public-url "$PUBLIC_URL" --api-url "$API_URL" --registry "$REGISTRY_URL" --ssl --cert "$CERT_PATH" --key "$KEY_PATH" > "logs/${AGENT_ID}_logs.txt" 2>&1 &
    
    # Store the process ID for later reference
    echo "$!" > "logs/${AGENT_ID}.pid"
    
    echo "$AGENT_ID started with PID $!"
    
    # Wait a few seconds between agent starts to avoid race conditions
    sleep 2
done

echo "All agents started successfully!"
echo "Use the following command to check if agents are running:"
echo "ps aux | grep run_ui_agent_https"
echo ""
echo "To stop all agents:"
echo 'for pid in logs/*.pid; do kill $(cat "$pid"); done' 

# Wait for 20 seconds before sending the email to ensure all the files are created
# sleep 20

# # Send agent links to the provided email
# if [ -n "$USER_EMAIL" ]; then
#     echo "Preparing to send agent links to $USER_EMAIL..."

#     # Collect all agent IDs
#     AGENT_IDS=()
#     for pidfile in "/opt/internet_of_agents/agents/logs/${AGENT_ID_PREFIX}"*.pid; do
#         AGENT_ID=$(basename "$pidfile" .pid)
#         AGENT_IDS+=("$AGENT_ID")
#     done

#     # Convert array to JSON format
#     AGENT_IDS_JSON=$(printf '%s\n' "${AGENT_IDS[@]}" | jq -R . | jq -s .)

#     # Send to the API endpoint
#     curl -X POST "https://chat.nanda-registry.com:6900/api/send-agent-links" \
#          -H "Content-Type: application/json" \
#          -d "{\"email\": \"$USER_EMAIL\", \"agentIds\": $AGENT_IDS_JSON}"

#     echo "Agent links sent to $USER_EMAIL via API"
# else
#     echo "USER_EMAIL not set. Skipping email notification."
# fi

wait