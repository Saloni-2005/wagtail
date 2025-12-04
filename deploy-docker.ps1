# Wagtail Demo Docker Deployment - Quick Start Script
# This script automates the Docker deployment process

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  Wagtail Demo Docker Deployment" -ForegroundColor Cyan
Write-Host "  Option 2, Method A - Custom Dockerfile" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
Write-Host "[1/6] Checking Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker found: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from https://www.docker.com/products/docker-desktop" -ForegroundColor Red
    exit 1
}

# Navigate to the project root
Write-Host ""
Write-Host "[2/6] Navigating to project directory..." -ForegroundColor Yellow
$projectRoot = "c:\Users\chaud\OneDrive\Documents\Desktop\wagtail"
if (Test-Path $projectRoot) {
    Set-Location $projectRoot
    Write-Host "✓ Changed to: $projectRoot" -ForegroundColor Green
} else {
    Write-Host "✗ Project directory not found: $projectRoot" -ForegroundColor Red
    exit 1
}

# Check if Dockerfile exists
Write-Host ""
Write-Host "[3/6] Checking for Dockerfile..." -ForegroundColor Yellow
$dockerfilePath = "demo\Dockerfile.custom"
if (Test-Path $dockerfilePath) {
    Write-Host "✓ Dockerfile found: $dockerfilePath" -ForegroundColor Green
} else {
    Write-Host "✗ Dockerfile not found: $dockerfilePath" -ForegroundColor Red
    Write-Host "Please ensure Dockerfile.custom exists in the demo directory" -ForegroundColor Red
    exit 1
}

# Stop and remove existing container if it exists
Write-Host ""
Write-Host "[4/6] Cleaning up existing containers..." -ForegroundColor Yellow
$existingContainer = docker ps -a -q -f name=wagtail-demo
if ($existingContainer) {
    Write-Host "Found existing container, removing..." -ForegroundColor Yellow
    docker stop wagtail-demo 2>$null
    docker rm wagtail-demo 2>$null
    Write-Host "✓ Existing container removed" -ForegroundColor Green
} else {
    Write-Host "✓ No existing container found" -ForegroundColor Green
}

# Build the Docker image
Write-Host ""
Write-Host "[5/6] Building Docker image..." -ForegroundColor Yellow
Write-Host "This may take 3-5 minutes on first build..." -ForegroundColor Cyan
Write-Host ""

docker build -f demo/Dockerfile.custom -t wagtail-demo-custom .

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✓ Docker image built successfully" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "✗ Docker build failed" -ForegroundColor Red
    Write-Host "Check the error messages above for details" -ForegroundColor Red
    exit 1
}

# Run the container
Write-Host ""
Write-Host "[6/6] Starting Docker container..." -ForegroundColor Yellow
docker run -d -p 8000:8000 --name wagtail-demo wagtail-demo-custom

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Container started successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to start container" -ForegroundColor Red
    exit 1
}

# Wait a moment for the container to initialize
Write-Host ""
Write-Host "Waiting for container to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check container status
Write-Host ""
Write-Host "Container status:" -ForegroundColor Cyan
docker ps -f name=wagtail-demo

# Show logs
Write-Host ""
Write-Host "Recent container logs:" -ForegroundColor Cyan
Write-Host "----------------------------------------" -ForegroundColor Gray
docker logs wagtail-demo --tail 20
Write-Host "----------------------------------------" -ForegroundColor Gray

# Success message
Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
Write-Host "  ✓ Deployment Complete!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Your Wagtail demo is now running!" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access your application:" -ForegroundColor Yellow
Write-Host "  • Main site:  http://localhost:8000" -ForegroundColor White
Write-Host "  • Admin:      http://localhost:8000/admin" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Create a superuser account:" -ForegroundColor White
Write-Host "     docker exec -it wagtail-demo python manage.py createsuperuser" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. View live logs:" -ForegroundColor White
Write-Host "     docker logs -f wagtail-demo" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. Stop the container:" -ForegroundColor White
Write-Host "     docker stop wagtail-demo" -ForegroundColor Gray
Write-Host ""
Write-Host "  4. Start the container again:" -ForegroundColor White
Write-Host "     docker start wagtail-demo" -ForegroundColor Gray
Write-Host ""
Write-Host "==================================================" -ForegroundColor Green
