#!/bin/bash

# Configure Remote N8N Connection
# Run this script to configure connection to remote N8N instance

set -e

echo "🔧 Configuring Remote N8N Connection..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get N8N machine IP
read -p "Enter the IP address of the N8N machine: " N8N_IP

if [ -z "$N8N_IP" ]; then
    echo -e "${RED}❌ IP address is required${NC}"
    exit 1
fi

echo "📝 Updating environment configuration..."

# Update .env file
if [ -f .env ]; then
    # Update existing .env
    sed -i "s|N8N_BASE_URL=.*|N8N_BASE_URL=http://${N8N_IP}:5678|g" .env
    sed -i "s|N8N_WEBHOOK_URL=.*|N8N_WEBHOOK_URL=http://${N8N_IP}:5678/webhook|g" .env
else
    # Create .env from example
    cp .env.example .env
    sed -i "s|IP_DO_NOTEBOOK|${N8N_IP}|g" .env
fi

echo "🧪 Testing N8N connection..."

# Test connection to N8N
N8N_URL="http://${N8N_IP}:5678"
API_KEY=$(grep N8N_API_KEY .env | cut -d '=' -f2)

echo "Testing connection to ${N8N_URL}..."

# Test basic connectivity
if curl -s --connect-timeout 5 "${N8N_URL}/healthz" > /dev/null; then
    echo -e "${GREEN}✅ N8N server is reachable${NC}"
else
    echo -e "${RED}❌ Cannot reach N8N server at ${N8N_URL}${NC}"
    echo "Make sure:"
    echo "  1. N8N is running on the remote machine"
    echo "  2. Port 5678 is accessible"
    echo "  3. No firewall blocking the connection"
    exit 1
fi

# Test API access
if curl -s -H "X-N8N-API-KEY: ${API_KEY}" "${N8N_URL}/api/v1/workflows" > /dev/null; then
    echo -e "${GREEN}✅ N8N API is accessible with provided key${NC}"
else
    echo -e "${YELLOW}⚠️  N8N API test failed - check API key${NC}"
    echo "You may need to:"
    echo "  1. Generate a new API key in N8N settings"
    echo "  2. Update the N8N_API_KEY in .env file"
fi

echo ""
echo "🎉 Remote N8N configuration completed!"
echo ""
echo "📊 Configuration:"
echo "  • N8N URL: http://${N8N_IP}:5678"
echo "  • API Key: ${API_KEY:0:20}..."
echo "  • Webhook URL: http://${N8N_IP}:5678/webhook"
echo ""
echo "🔧 Updated files:"
echo "  • .env (N8N URLs updated)"
echo ""
echo "💡 Next steps:"
echo "  1. Run './scripts/setup-complete.sh' to start local services"
echo "  2. Execute development agents to create N8N workflows"
echo ""