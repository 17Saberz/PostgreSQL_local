# PostgreSQL_local

A simple Flask + SQLAlchemy + PostgreSQL application for local database operations and form handling. This project demonstrates how to manage notes and tags using a basic web interface.

## Features

- Flask web application
- SQLAlchemy ORM integration with PostgreSQL
- WTForms for form handling
- Notes and Tags management
- Jinja2 templating
- Bootstrap styling

## Getting Started

### 1. Clone this repository

```bash
git clone https://github.com/17Saberz/PostgreSQL_local.git
cd PostgreSQL_local
```

### 2. Set up a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL
Make sure PostgreSQL is installed and running on your machine. Create a new database and configure your credentials in config.py or via environment variables.

### 5. Run the app
```bash
python psunote/noteapp.py
```

The app will be available at http://127.0.0.1:5000/
