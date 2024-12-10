# Quick Start Guide for VerdunNRP

## Prerequisites
- Python 3.8+
- Django 3.2+
- PostgreSQL 12+

## Installation Steps

1. Clone the repository
```bash
git clone https://github.com/your-org/VerdunNRP.git
cd VerdunNRP
```

2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure database
```bash
# Update database settings in settings.py
python manage.py migrate
```

5. Create superuser
```bash
python manage.py createsuperuser
```

6. Run development server
```bash
python manage.py runserver
```

## First Steps
- Log in to the admin panel
- Create your first economic agents
- Explore the value network interface

## Troubleshooting
- Check [installation guide](/getting_started/installation.md) for detailed instructions
- Consult [technical documentation](/technical/README.md) for in-depth information

## Need Help?
- Join our community discussion
- File an issue on GitHub
- Consult the [user guide](/user_guide/README.md)
