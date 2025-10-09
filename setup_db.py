from app import create_app, db

def setup_database():
    """Create all database tables."""
    app = create_app()
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created.")

if __name__ == '__main__':
    setup_database()