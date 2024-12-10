# Installation Guide

This guide provides detailed instructions for setting up VerdunNRP in different environments.

## Prerequisites

- Docker
- Python 3.x
- Git

## Installation Methods

### 1. Docker Installation (Recommended)

1. Install Docker following the [official Docker documentation](https://docs.docker.com/installation/)

2. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/VerdunNRP.git
   cd VerdunNRP
   ```

3. Build and run using Docker:
   ```bash
   docker build -t verdunnrp .
   docker run -p 8000:8000 verdunnrp
   ```

### 2. Local Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the database:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

### 3. Vagrant Setup (For Windows/Mac Users)

If you're using Windows or Mac OS X, you can use Vagrant to run a Linux virtual machine:

1. Install Vagrant from the [official website](https://www.vagrantup.com/downloads.html)

2. Start the Vagrant box:
   ```bash
   vagrant up
   vagrant ssh
   ```

3. Follow the Docker installation steps inside the Vagrant box

## Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Update the environment variables in `.env` with your settings

## Verification

1. Access the application at `http://localhost:8000`
2. Log in with your superuser credentials
3. Verify that you can access the admin interface at `http://localhost:8000/admin`

## Common Issues and Solutions

See our [troubleshooting guide](../technical/troubleshooting.md) for common issues and their solutions.

## Next Steps

- Read the [Basic Usage Guide](basic_usage.md)
- Configure your [Environment Settings](../configuration/environment.md)
- Learn about [Contributing](../development/contributing.md)
