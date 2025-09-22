#!/bin/bash

# Gehenna Professional Application Startup Script
# This script helps you quickly start the application in different modes

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[GEHENNA]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check Docker
check_docker() {
    if ! command_exists docker; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! command_exists docker-compose; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi

    print_status "Docker and Docker Compose are available"
}

# Function to show help
show_help() {
    echo "Gehenna Professional Application Startup Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  dev      Start in development mode (local Python)"
    echo "  prod     Start in production mode (Docker)"
    echo "  build    Build Docker images only"
    echo "  logs     Show application logs"
    echo "  stop     Stop all services"
    echo "  clean    Stop services and remove volumes"
    echo "  help     Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 dev   # Start development environment"
    echo "  $0 prod  # Start production environment"
    echo "  $0 logs  # View application logs"
}

# Function to start development environment
start_development() {
    print_header "Starting Gehenna in Development Mode"
    print_warning "Make sure MongoDB is running on localhost:27017"

    # Check if Python virtual environment exists
    if [ ! -d "venv" ]; then
        print_status "Creating Python virtual environment..."
        python3 -m venv venv
    fi

    # Activate virtual environment
    source venv/bin/activate

    print_status "Installing backend dependencies..."
    cd backend
    pip install -r requirements.txt
    cd ..

    print_status "Installing frontend dependencies..."
    cd frontend
    pip install -r requirements.txt
    cd ..

    print_status "Starting backend service..."
    cd backend
    export MONGO_URL="mongodb://localhost:27017"
    export PORT=8002
    export DEBUG=true
    python app.py &
    BACKEND_PID=$!
    cd ..

    print_status "Starting frontend service..."
    cd frontend
    export BACKEND_URL="http://localhost:8002"
    export PORT=8001
    export DEBUG=true
    python app.py &
    FRONTEND_PID=$!
    cd ..

    print_status "Development environment started!"
    echo ""
    echo "Frontend: http://localhost:8001"
    echo "Backend API: http://localhost:8002"
    echo "Health Check: http://localhost:8002/health"
    echo ""
    echo "Press Ctrl+C to stop services"

    # Wait for user interrupt
    trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
    wait
}

# Function to start production environment
start_production() {
    print_header "Starting Gehenna in Production Mode"

    check_docker

    # Create .env file if it doesn't exist
    if [ ! -f ".env" ]; then
        print_warning "Creating .env file from template..."
        cp .env.example .env
        print_warning "Please edit .env file with your configuration before running in production"
        read -p "Do you want to continue with default settings? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_status "Please edit .env file and run again"
            exit 0
        fi
    fi

    print_status "Building and starting services..."
    docker-compose up --build -d

    print_status "Waiting for services to be healthy..."
    sleep 10

    # Check if services are running
    if docker-compose ps | grep -q "Up"; then
        print_status "Production environment started successfully!"
        echo ""
        echo "Frontend: http://localhost:8001"
        echo "Backend API: http://localhost:8002"
        echo "Mongo Express: http://localhost:8081"
        echo "Health Check: http://localhost:8002/health"
        echo ""
        echo "View logs: $0 logs"
        echo "Stop services: $0 stop"
    else
        print_error "Some services failed to start. Check logs with: $0 logs"
        exit 1
    fi
}

# Function to build Docker images
build_images() {
    print_header "Building Docker Images"

    check_docker

    print_status "Building backend image..."
    docker build -t gehenna-backend:latest ./backend

    print_status "Building frontend image..."
    docker build -t gehenna-frontend:latest ./frontend

    print_status "Images built successfully!"
    echo ""
    echo "Run 'docker-compose up' to start the application"
}

# Function to show logs
show_logs() {
    print_header "Application Logs"

    check_docker

    if docker-compose ps | grep -q "Up"; then
        echo "Choose log type:"
        echo "1) All services"
        echo "2) Backend only"
        echo "3) Frontend only"
        echo "4) MongoDB only"
        read -p "Enter choice (1-4): " choice

        case $choice in
            1) docker-compose logs -f ;;
            2) docker-compose logs -f backend ;;
            3) docker-compose logs -f frontend ;;
            4) docker-compose logs -f mongo ;;
            *) print_error "Invalid choice" ;;
        esac
    else
        print_warning "No running services found. Start with: $0 prod"
    fi
}

# Function to stop services
stop_services() {
    print_header "Stopping Services"

    if docker-compose ps | grep -q "Up"; then
        docker-compose stop
        print_status "Services stopped successfully"
    else
        print_warning "No running services found"
    fi
}

# Function to clean up
clean_up() {
    print_header "Cleaning Up"

    stop_services

    read -p "This will remove all containers, networks, and volumes. Continue? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose down -v --remove-orphans
        docker system prune -f
        print_status "Cleanup completed"
    fi
}

# Main script logic
case "${1:-help}" in
    "dev")
        start_development
        ;;
    "prod")
        start_production
        ;;
    "build")
        build_images
        ;;
    "logs")
        show_logs
        ;;
    "stop")
        stop_services
        ;;
    "clean")
        clean_up
        ;;
    "help"|*)
        show_help
        ;;
esac
