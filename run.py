from app import create_app, db, socketio

app = create_app()

if __name__ == "__main__":
    # The allow_unsafe_werkzeug=True flag is for development purposes only.
    # For production, it is recommended to use a production-ready WSGI server like Gunicorn or uWSGI.
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True, use_reloader=False)
