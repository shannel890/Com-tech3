"""
Tests for form validation.
"""
import pytest
from app.form import RegistrationForm, LoginForm, GroupForm, MessageForm


class TestRegistrationForm:
    """Tests for the RegistrationForm."""

    def test_valid_registration_form(self, app):
        """Test registration form with valid data."""
        with app.test_request_context():
            form = RegistrationForm(
                first_name='John',
                last_name='Doe',
                email='john@example.com',
                password='password123',
                confirm_password='password123'
            )
            assert form.validate()

    def test_password_mismatch(self, app):
        """Test registration form with mismatched passwords."""
        with app.test_request_context():
            form = RegistrationForm(
                first_name='John',
                last_name='Doe',
                email='john@example.com',
                password='password123',
                confirm_password='different'
            )
            assert not form.validate()
            assert 'confirm_password' in form.errors

    def test_invalid_email(self, app):
        """Test registration form with invalid email."""
        with app.test_request_context():
            form = RegistrationForm(
                first_name='John',
                last_name='Doe',
                email='not-an-email',
                password='password123',
                confirm_password='password123'
            )
            assert not form.validate()
            assert 'email' in form.errors

    def test_missing_required_fields(self, app):
        """Test registration form with missing required fields."""
        with app.test_request_context():
            form = RegistrationForm()
            assert not form.validate()
            assert 'first_name' in form.errors
            assert 'last_name' in form.errors
            assert 'email' in form.errors
            assert 'password' in form.errors


class TestLoginForm:
    """Tests for the LoginForm."""

    def test_valid_login_form(self, app):
        """Test login form with valid data."""
        with app.test_request_context():
            form = LoginForm(
                email='user@example.com',
                password='password123'
            )
            assert form.validate()

    def test_invalid_email_format(self, app):
        """Test login form with invalid email format."""
        with app.test_request_context():
            form = LoginForm(
                email='invalid-email',
                password='password123'
            )
            assert not form.validate()
            assert 'email' in form.errors

    def test_missing_password(self, app):
        """Test login form with missing password."""
        with app.test_request_context():
            form = LoginForm(
                email='user@example.com',
                password=''
            )
            assert not form.validate()
            assert 'password' in form.errors


class TestGroupForm:
    """Tests for the GroupForm."""

    def test_valid_group_form(self, app):
        """Test group form with valid data."""
        with app.test_request_context():
            form = GroupForm(
                name='Study Group',
                description='A group for studying together'
            )
            assert form.validate()

    def test_group_name_too_long(self, app):
        """Test group form with name exceeding max length."""
        with app.test_request_context():
            form = GroupForm(
                name='A' * 101,  # Exceeds max length of 100
                description='Description'
            )
            assert not form.validate()
            assert 'name' in form.errors

    def test_description_too_long(self, app):
        """Test group form with description exceeding max length."""
        with app.test_request_context():
            form = GroupForm(
                name='Group',
                description='D' * 301  # Exceeds max length of 300
            )
            assert not form.validate()
            assert 'description' in form.errors

    def test_missing_group_name(self, app):
        """Test group form with missing name."""
        with app.test_request_context():
            form = GroupForm(
                description='Description only'
            )
            assert not form.validate()
            assert 'name' in form.errors


class TestMessageForm:
    """Tests for the MessageForm."""

    def test_valid_message_form(self, app):
        """Test message form with valid data."""
        with app.test_request_context():
            form = MessageForm(
                content='Hello, this is a test message!'
            )
            assert form.validate()

    def test_message_too_long(self, app):
        """Test message form with content exceeding max length."""
        with app.test_request_context():
            form = MessageForm(
                content='M' * 501  # Exceeds max length of 500
            )
            assert not form.validate()
            assert 'content' in form.errors

    def test_empty_message(self, app):
        """Test message form with empty content."""
        with app.test_request_context():
            form = MessageForm(
                content=''
            )
            assert not form.validate()
            assert 'content' in form.errors
