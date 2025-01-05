# VerdunNRP Documentation

> ⚠️ **Archived Project Notice**: This is an archived project that will not receive further updates. This documentation serves as a reference for understanding the project's architecture and implementation.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
   - [Core Components](#core-components)
   - [Technology Stack](#technology-stack)
   - [Security](#security)
3. [Technical Documentation](#technical-documentation)
   - [API Reference](technical/api.md)
   - [Database Schema](technical/database.md)
4. [System Requirements](#system-requirements)
5. [Quick Start](#quick-start)

## Project Overview

VerdunNRP is a Django-based Network Resource Planning system designed to manage complex economic interactions. The system handles equipment management, resource tracking, and value network operations.

[↑ Back to Top](#table-of-contents)

## Architecture

### Core Components

1. **Equipment Module**
   - Manages equipment inventory and usage
   - Handles usage logging and payment processing
   - Tracks maintenance and repairs

2. **Resource Module**
   - Manages resource types and inventory
   - Tracks resource movements and transfers
   - Calculates resource values

3. **Board Module**
   - Manages workflows and processes
   - Tracks resource allocation
   - Handles stage progression

[↑ Back to Top](#table-of-contents)

### Technology Stack

- **Backend**: Django 3.2+
- **Database**: PostgreSQL
- **Cache**: Redis
- **API**: RESTful with token authentication

[↑ Back to Top](#table-of-contents)

### Security

- Token-based authentication
- Role-based access control
- CSRF protection
- Session management

[↑ Back to Top](#table-of-contents)

## Technical Documentation

Detailed technical documentation is split into two main sections:

- [API Reference](technical/api.md) - Complete API documentation
  - Authentication
  - Endpoints
  - Request/Response formats
  - Error handling

- [Database Schema](technical/database.md) - Database documentation
  - Table structures
  - Relationships
  - Common queries

[↑ Back to Top](#table-of-contents)

## System Requirements

- Python 3.9+
- PostgreSQL 12+
- Redis 6+

[↑ Back to Top](#table-of-contents)

## Quick Start

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure database settings
4. Run migrations: `python manage.py migrate`
5. Start server: `python manage.py runserver`

[↑ Back to Top](#table-of-contents)

## License

[Insert License Information]
