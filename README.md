# Com-Tech

Com-Tech is a web-based communication platform that allows users to create groups, chat with other users, and engage in video and audio calls. This project is built with Flask and uses a number of extensions to provide a rich feature set.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Setup and Installation](#setup-and-installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [Project Structure](#project-structure)
- [Development Notes](#development-notes)
- [Contributing](#contributing)
- [License](#license)

## Features

*   **User Authentication**: Secure registration and login system with password hashing
*   **Group Management**: Create and manage communication groups
*   **Real-time Chat**: Instant messaging with Socket.IO integration
*   **User Dashboard**: Intuitive interface to manage contacts and groups
*   **Contact Management**: Add and organize your contacts
*   **Video/Audio Calls**: (Coming Soon) Real-time video and audio communication

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLAlchemy with SQLite (configurable for PostgreSQL/MySQL)
- **Authentication**: Flask-Login with Werkzeug password hashing
- **Real-time Communication**: Flask-SocketIO
- **Forms**: Flask-WTF with CSRF protection
- **Database Migrations**: Flask-Migrate
- **Internationalization**: Flask-Babel
- **Frontend**: HTML, CSS, JavaScript with DaisyUI/Tailwind CSS

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment support (recommended)

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/shannel890/Com-tech3.git
    cd Com-tech3
    ```

2.  **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**

    Create a `.env` file in the root directory with the following variables:

    ```env
    SECRET_KEY=your-secret-key-here
    DATABASE_URL=sqlite:///app.db
    SECURITY_PASSWORD_SALT=your-password-salt-here
    ```

    **Note**: Generate secure random values for `SECRET_KEY` and `SECURITY_PASSWORD_SALT` in production.

5.  **Initialize the database:**

    This project uses Flask-Migrate to manage database schemas. Run the following commands:

    ```bash
    export FLASK_APP=run.py  # On Windows, use `set FLASK_APP=run.py`
    flask db upgrade
    ```

    Alternatively, you can use the setup script:

    ```bash
    python setup_db.py
    ```

6.  **Run the application:**

    ```bash
    python run.py
    ```

    The application will be available at `http://127.0.0.1:5000`.

## Configuration

The application configuration is managed through the `config.py` file and environment variables:

- **SECRET_KEY**: Flask secret key for session management (required)
- **DATABASE_URL**: Database connection string (defaults to SQLite)
- **SECURITY_PASSWORD_SALT**: Salt for password hashing (required)

For production deployment, ensure you:
- Use strong, randomly generated keys
- Configure a production-grade database (PostgreSQL recommended)
- Set `DEBUG=False`
- Use a production WSGI server (Gunicorn, uWSGI)

## Usage

### Registering a New User

1. Navigate to `http://127.0.0.1:5000/auth/register`
2. Fill in your details (first name, last name, email, password)
3. Click "Register"
4. You'll be redirected to the login page

### Creating a Group

1. Log in to your account
2. Navigate to the dashboard
3. Click "Create New Group"
4. Enter group name and description
5. Click "Create Group"

### Chatting in Groups

1. From the dashboard, click on a group
2. Click "Chat" to open the chat interface
3. Type your message and click "Send"

## Running Tests

To run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest

# Run with coverage report
pytest --cov=app tests/

# Run specific test file
pytest tests/test_models.py
```

## Project Structure

```
Com-tech3/
├── app/
│   ├── __init__.py           # Application factory
│   ├── api/                  # API routes
│   ├── auth/                 # Authentication routes
│   ├── dashboard/            # Dashboard routes
│   ├── extension.py          # Flask extensions
│   ├── form.py              # WTForms definitions
│   ├── models/              # Database models
│   ├── routes.py            # Main routes
│   ├── socket_events.py     # Socket.IO events
│   ├── sockets.py           # Socket.IO handlers
│   └── templates/           # HTML templates
├── instance/                # Instance-specific files (gitignored)
├── migrations/              # Database migrations
├── tests/                   # Test suite
├── .env                     # Environment variables (gitignored)
├── .gitignore              # Git ignore rules
├── config.py               # Application configuration
├── requirements.txt        # Python dependencies
├── run.py                  # Application entry point
└── setup_db.py            # Database setup script
```

## Development Notes

### Development Server

The application is configured to run in debug mode, which provides:
- Helpful error messages
- Automatic code reloading
- Interactive debugger

**Important**: The Werkzeug development server is NOT suitable for production use.

The `run.py` script includes the `allow_unsafe_werkzeug=True` flag to bypass production warnings. This is for development purposes only.

### Production Deployment

For production deployment:

1. Set environment variables properly
2. Use a production WSGI server:

   ```bash
   # Using Gunicorn
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 'app:create_app()'
   ```

3. Configure a reverse proxy (nginx, Apache)
4. Set up SSL/TLS certificates
5. Configure proper logging
6. Use a production database (PostgreSQL, MySQL)

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.