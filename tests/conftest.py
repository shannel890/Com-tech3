"""
Test configuration and fixtures for Com-Tech test suite.
"""
import pytest
import os
import sys
from app import create_app, db
from app.models.user import User
from app.models.group import Group
from config import Config


class TestConfig(Config):
    """Test configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key'
    SECURITY_PASSWORD_SALT = 'test-salt'


@pytest.fixture
def app():
    """Create and configure a test Flask application instance."""
    app = create_app()
    app.config.from_object(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Create a test client for the Flask application."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner for the Flask application."""
    return app.test_cli_runner()


@pytest.fixture
def test_user(app):
    """Create a test user."""
    with app.app_context():
        user = User(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='testpassword123'
        )
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture
def test_group(app, test_user):
    """Create a test group."""
    with app.app_context():
        user = User.query.filter_by(email='test@example.com').first()
        group = Group(
            name='Test Group',
            description='This is a test group',
            owner_id=user.id
        )
        db.session.add(group)
        db.session.commit()
        return group
