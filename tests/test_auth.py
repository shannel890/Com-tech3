"""
Tests for authentication routes.
"""
import pytest
from app.models.user import User
from app import db


class TestAuthRoutes:
    """Tests for authentication routes."""

    def test_register_page_loads(self, client):
        """Test that the registration page loads successfully."""
        response = client.get('/auth/register')
        assert response.status_code == 200
        assert b'Register' in response.data

    def test_login_page_loads(self, client):
        """Test that the login page loads successfully."""
        response = client.get('/auth/login')
        assert response.status_code == 200
        assert b'Login' in response.data

    def test_user_registration(self, client, app):
        """Test user registration with valid data."""
        response = client.post('/auth/register', data={
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password': 'securepassword',
            'confirm_password': 'securepassword'
        }, follow_redirects=True)

        with app.app_context():
            user = User.query.filter_by(email='newuser@example.com').first()
            assert user is not None
            assert user.first_name == 'New'
            assert user.last_name == 'User'

    def test_user_login_success(self, client, test_user):
        """Test user login with correct credentials."""
        response = client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'testpassword123',
            'remember': False
        }, follow_redirects=True)

        assert response.status_code == 200
        # Should redirect to dashboard after successful login
        assert b'dashboard' in response.request.path.encode() or b'Dashboard' in response.data

    def test_user_login_failure(self, client):
        """Test user login with incorrect credentials."""
        response = client.post('/auth/login', data={
            'email': 'wrong@example.com',
            'password': 'wrongpassword',
            'remember': False
        }, follow_redirects=True)

        assert response.status_code == 200
        # Should remain on login page after failed login
        assert b'Login' in response.data or b'login' in response.data

    def test_registration_password_mismatch(self, client):
        """Test registration fails when passwords don't match."""
        response = client.post('/auth/register', data={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test2@example.com',
            'password': 'password123',
            'confirm_password': 'password456'
        }, follow_redirects=True)

        assert response.status_code == 200
        # Form validation should prevent registration
        assert b'Register' in response.data

    def test_registration_invalid_email(self, client):
        """Test registration fails with invalid email."""
        response = client.post('/auth/register', data={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'not-an-email',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)

        assert response.status_code == 200
        # Should stay on registration page
        assert b'Register' in response.data

    def test_logout(self, client, test_user):
        """Test user logout."""
        # First login
        client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'testpassword123',
            'remember': False
        })

        # Then logout
        response = client.get('/auth/logout', follow_redirects=True)
        assert response.status_code == 200
