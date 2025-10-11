"""
Tests for database models.
"""
import pytest
from app.models.user import User
from app.models.group import Group
from app import db


class TestUserModel:
    """Tests for the User model."""

    def test_user_creation(self, app):
        """Test creating a new user."""
        with app.app_context():
            user = User(
                first_name='John',
                last_name='Doe',
                email='john.doe@example.com',
                password='securepassword'
            )
            db.session.add(user)
            db.session.commit()

            assert user.id is not None
            assert user.first_name == 'John'
            assert user.last_name == 'Doe'
            assert user.email == 'john.doe@example.com'
            assert user.password_hash is not None

    def test_password_hashing(self, app):
        """Test that passwords are properly hashed."""
        with app.app_context():
            user = User(
                first_name='Jane',
                last_name='Smith',
                email='jane@example.com',
                password='mypassword'
            )
            db.session.add(user)
            db.session.commit()

            # Password should be hashed, not stored in plain text
            assert user.password_hash != 'mypassword'
            # Should be able to verify the password
            assert user.verify_password('mypassword')
            # Should reject incorrect password
            assert not user.verify_password('wrongpassword')

    def test_password_not_readable(self, app):
        """Test that password attribute raises error when accessed."""
        with app.app_context():
            user = User(
                first_name='Test',
                last_name='User',
                email='test@example.com',
                password='password'
            )
            with pytest.raises(AttributeError):
                _ = user.password

    def test_user_name_property(self, app):
        """Test the user's full name property."""
        with app.app_context():
            user = User(
                first_name='John',
                last_name='Doe',
                email='john@example.com',
                password='password'
            )
            assert user.name == 'John Doe'

    def test_unique_email_constraint(self, app):
        """Test that email must be unique."""
        with app.app_context():
            user1 = User(
                first_name='User',
                last_name='One',
                email='same@example.com',
                password='password1'
            )
            user2 = User(
                first_name='User',
                last_name='Two',
                email='same@example.com',
                password='password2'
            )
            db.session.add(user1)
            db.session.commit()

            db.session.add(user2)
            with pytest.raises(Exception):  # Should raise IntegrityError
                db.session.commit()


class TestGroupModel:
    """Tests for the Group model."""

    def test_group_creation(self, app, test_user):
        """Test creating a new group."""
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            group = Group(
                name='Study Group',
                description='A group for studying',
                owner_id=user.id
            )
            db.session.add(group)
            db.session.commit()

            assert group.id is not None
            assert group.name == 'Study Group'
            assert group.description == 'A group for studying'
            assert group.owner_id == user.id

    def test_group_owner_relationship(self, app, test_user):
        """Test the relationship between group and owner."""
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            group = Group(
                name='My Group',
                description='Test group',
                owner_id=user.id
            )
            db.session.add(group)
            db.session.commit()

            # Refresh the user object
            db.session.refresh(user)
            assert group.owner.id == user.id
            assert len(user.groups) > 0

    def test_unique_group_name(self, app, test_user):
        """Test that group names must be unique."""
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            group1 = Group(
                name='Unique Group',
                description='First group',
                owner_id=user.id
            )
            group2 = Group(
                name='Unique Group',
                description='Second group',
                owner_id=user.id
            )
            db.session.add(group1)
            db.session.commit()

            db.session.add(group2)
            with pytest.raises(Exception):  # Should raise IntegrityError
                db.session.commit()
