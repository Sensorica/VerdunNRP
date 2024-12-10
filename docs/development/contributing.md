# Contributing to VerdunNRP

This guide will help you get started with contributing to VerdunNRP.

## Development Setup

### Prerequisites

- Python 3.x
- PostgreSQL
- Git
- Docker (optional)
- Vagrant (optional for Windows/Mac users)

### Local Development Environment

1. Clone the repository:
```bash
git clone https://github.com/your-repo/VerdunNRP.git
cd VerdunNRP
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

## Code Organization

### Core Components

- `valuenetwork/`: Main application directory
  - `models.py`: Core data models based on REA
  - `views.py`: View logic
  - `api/`: REST API implementation
  - `valueaccounting/`: Core accounting logic

- `account/`: User account management
- `board/`: Dashboard and UI components
- `equipment/`: Equipment management

### Key Files

- `requirements.txt`: Python dependencies
- `manage.py`: Django management script
- `Dockerfile`: Docker configuration
- `settings.py`: Application settings

## Coding Standards

### Python Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for classes and functions
- Keep functions focused and small

### Documentation

- Update relevant documentation when making changes
- Include docstrings in Python code
- Document API changes in the API documentation
- Update README.md when appropriate

### Testing

- Write tests for new features
- Update existing tests when modifying code
- Run the test suite before submitting changes:
```bash
python manage.py test
```

## Git Workflow

1. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes:
- Write code
- Add tests
- Update documentation

3. Commit your changes:
```bash
git add .
git commit -m "Description of changes"
```

4. Push to your fork:
```bash
git push origin feature/your-feature-name
```

5. Create a Pull Request

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb in present tense
- Reference issues when applicable

Example:
```
Add user authentication to API endpoints

- Implement token-based authentication
- Add user permission checks
- Update API documentation

Fixes #123
```

## Pull Request Process

1. Update documentation
2. Add or update tests
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Development Tools

### Recommended IDE Setup

- VS Code with Python extension
- PyCharm Professional/Community
- Sublime Text with Python packages

### Useful Commands

Development server:
```bash
python manage.py runserver
```

Create migrations:
```bash
python manage.py makemigrations
```

Apply migrations:
```bash
python manage.py migrate
```

## Getting Help

- Check existing documentation
- Search issues on GitHub
- Join the development community
- Contact maintainers

## License

By contributing to VerdunNRP, you agree that your contributions will be licensed under its license terms.
