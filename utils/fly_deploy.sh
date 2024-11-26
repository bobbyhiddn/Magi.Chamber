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

# Function to check health endpoint with retries
check_health() {
    local url="$1"
    local max_attempts=10
    local wait_time=10
    local attempt=1

    print_status "Checking deployment health..."
    
    while [ $attempt -le $max_attempts ]; do
        print_status "Attempt $attempt of $max_attempts"
        
        if curl -s "${url}/health" | grep -q "operational"; then
            print_success "Chamber is operational!"
            return 0
        else
            print_status "Chamber is still starting up, waiting ${wait_time} seconds..."
            sleep $wait_time
            attempt=$((attempt + 1))
        fi
    done

    print_error "Chamber failed to respond after $max_attempts attempts"
    return 1
}

# Load .env file
if [ -f .env ]; then
    print_status "Loading environment variables..."
    export $(grep -v '^#' .env | xargs)
    print_success "Environment variables loaded"
else
    print_error ".env file not found!"
fi

# Update submodules before deployment
print_status "Updating submodules..."
git pull --recurse-submodules
git submodule update --init --recursive
print_success "Submodules updated"

# Set the secrets using flyctl
print_status "Setting secrets on Fly.io..."
flyctl secrets set \
    FLASK_SECRET_KEY="$FLASK_SECRET_KEY" \
    CHAMBER_API_KEY="$CHAMBER_API_KEY" \
    WEBHOOK_SECRET="$WEBHOOK_SECRET"

print_success "Secrets set successfully on Fly.io!"

# Deploy to Fly.io
print_status "Deploying Magi.Chamber to Fly.io..."
if fly deploy; then
    print_success "Chamber has materialized in the cloud!"
    
    # Get the app URL
    APP_URL="magi-chamber.fly.dev"
    print_status "Your chamber awaits at: https://$APP_URL"
    
    # Check health with retries
    check_health "https://$APP_URL"
else
    print_error "Deployment failed"
fi

# Show recent logs regardless of health check result
print_status "Recent logs from the Chamber:"
fly logs