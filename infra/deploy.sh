#!/bin/bash

# Digital Medical Report Organizer Deployment Script
# This script handles the deployment of the entire application stack

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.yml"
ENV_FILE=".env"

echo -e "${GREEN}🏥 Digital Medical Report Organizer Deployment${NC}"
echo "================================================"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed. Please install Docker Compose first.${NC}"
    exit 1
fi

# Check if .env file exists
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${YELLOW}⚠️  .env file not found. Creating from .env.example...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please update the .env file with your configuration before continuing.${NC}"
    read -p "Press Enter to continue after updating .env file..."
fi

# Function to check if services are healthy
check_health() {
    local service=$1
    local max_attempts=30
    local attempt=1
    
    echo -e "${YELLOW}🔍 Checking health of $service...${NC}"
    
    while [ $attempt -le $max_attempts ]; do
        if docker-compose -f $COMPOSE_FILE ps $service | grep -q "healthy"; then
            echo -e "${GREEN}✅ $service is healthy${NC}"
            return 0
        fi
        
        echo -e "${YELLOW}⏳ Waiting for $service to be healthy (attempt $attempt/$max_attempts)...${NC}"
        sleep 10
        ((attempt++))
    done
    
    echo -e "${RED}❌ $service failed to become healthy${NC}"
    return 1
}

# Function to build and start services
deploy_services() {
    echo -e "${GREEN}🚀 Building and starting services...${NC}"
    
    # Pull latest images
    echo -e "${YELLOW}📥 Pulling latest images...${NC}"
    docker-compose -f $COMPOSE_FILE pull
    
    # Build custom images
    echo -e "${YELLOW}🔨 Building custom images...${NC}"
    docker-compose -f $COMPOSE_FILE build --no-cache
    
    # Start services
    echo -e "${YELLOW}🚀 Starting services...${NC}"
    docker-compose -f $COMPOSE_FILE up -d
    
    # Wait for services to be healthy
    check_health "postgres"
    check_health "redis"
    check_health "backend"
    
    echo -e "${GREEN}✅ All services are running!${NC}"
}

# Function to show service status
show_status() {
    echo -e "${GREEN}📊 Service Status:${NC}"
    docker-compose -f $COMPOSE_FILE ps
    
    echo -e "\n${GREEN}🌐 Application URLs:${NC}"
    echo "Frontend: http://localhost:3000"
    echo "Backend API: http://localhost:8000"
    echo "API Docs: http://localhost:8000/docs"
    echo "Health Check: http://localhost:8000/health"
}

# Function to show logs
show_logs() {
    local service=$1
    if [ -z "$service" ]; then
        echo -e "${GREEN}📋 All Service Logs:${NC}"
        docker-compose -f $COMPOSE_FILE logs -f
    else
        echo -e "${GREEN}📋 $service Logs:${NC}"
        docker-compose -f $COMPOSE_FILE logs -f $service
    fi
}

# Function to stop services
stop_services() {
    echo -e "${YELLOW}🛑 Stopping services...${NC}"
    docker-compose -f $COMPOSE_FILE down
    echo -e "${GREEN}✅ Services stopped${NC}"
}

# Function to clean up
cleanup() {
    echo -e "${YELLOW}🧹 Cleaning up...${NC}"
    docker-compose -f $COMPOSE_FILE down -v
    docker system prune -f
    echo -e "${GREEN}✅ Cleanup completed${NC}"
}

# Main script logic
case "${1:-deploy}" in
    "deploy")
        deploy_services
        show_status
        ;;
    "status")
        show_status
        ;;
    "logs")
        show_logs $2
        ;;
    "stop")
        stop_services
        ;;
    "restart")
        stop_services
        deploy_services
        show_status
        ;;
    "cleanup")
        cleanup
        ;;
    "help")
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  deploy   - Deploy all services (default)"
        echo "  status   - Show service status"
        echo "  logs     - Show logs (optionally specify service name)"
        echo "  stop     - Stop all services"
        echo "  restart  - Restart all services"
        echo "  cleanup  - Stop services and clean up volumes"
        echo "  help     - Show this help message"
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        echo "Use '$0 help' to see available commands"
        exit 1
        ;;
esac
