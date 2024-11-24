#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to print status messages
print_status() {
    echo -e "${YELLOW}>>> $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
    exit 1
}

# Load .env file
if [ -f .env ]; then
    print_status "Loading environment variables..."
    export $(grep -v '^#' .env | xargs)
    print_success "Environment variables loaded"
else
    print_error ".env file not found!"
fi

# Set the secrets using flyctl
print_status "Setting secrets on Fly.io..."
flyctl secrets set \
    FLASK_SECRET_KEY="$FLASK_SECRET_KEY" \
    FLASK_ENV="$FLASK_ENV"

print_success "Secrets set successfully on Fly.io!"

# Deploy to Fly.io
print_status "Deploying Magi.Chamber to Fly.io..."
if fly deploy; then
    print_success "Chamber has materialized in the cloud!"
    
    # Get the app URL
    APP_URL=$(flyctl status --json | jq -r '.application.hostname')
    print_status "Your chamber awaits at: https://$APP_URL"
    
    # Quick health check
    if curl -s "https://$APP_URL/health" | grep -q "operational"; then
        print_success "Chamber is operational and ready for spells!"
    else
        print_error "Chamber deployment seems unstable. Check 'flyctl logs'"
    fi
else
    print_error "Deployment failed"
fi