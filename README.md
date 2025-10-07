# Com-Tech

Com-Tech is a web-based communication platform that allows users to create groups, chat with other users, and engage in video and audio calls. This project is built with Flask and uses a number of extensions to provide a rich feature set.

## Features

*   User registration and authentication
*   Group creation and management
*   Real-time chat with Socket.IO
*   A user-friendly dashboard to manage contacts and groups
*   (Coming Soon) Video and audio calls

## Setup and Installation

To get started with the project, you'll need to have Python and pip installed. Then, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/com-tech.git
    cd com-tech
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

4.  **Set up the database:**

    This project uses Flask-Migrate to manage database schemas. To initialize the database and apply the migrations, run the following commands:

    ```bash
    export FLASK_APP=run.py  # On Windows, use `set FLASK_APP=run.py`
    flask db upgrade
    ```

5.  **Run the application:**

    ```bash
    python run.py
    ```

    The application will be available at `http://127.0.0.1:5000`.

## Development Notes

The application is configured to run in debug mode, which provides helpful error messages and live reloading. However, the Werkzeug development server is not suitable for production use. For deployment, it is recommended to use a production-ready WSGI server like Gunicorn or uWSGI.

To run the application with the development server, you can use the `run.py` script, which includes the `allow_unsafe_werkzeug=True` flag to bypass the production server check. This is for development purposes only.