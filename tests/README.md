"""
Com-Tech Test Suite

This directory contains tests for the Com-Tech application.

## Test Structure

- `conftest.py`: Test configuration and fixtures
- `test_models.py`: Tests for database models
- `test_auth.py`: Tests for authentication routes
- `test_forms.py`: Tests for form validation

## Running Tests

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

Run specific test file:
```bash
pytest tests/test_models.py
```

Run specific test:
```bash
pytest tests/test_models.py::TestUserModel::test_user_creation
```

Run with verbose output:
```bash
pytest -v
```

## Writing Tests

When adding new tests:

1. Follow the existing test structure
2. Use descriptive test names
3. Include docstrings explaining what is being tested
4. Use fixtures from `conftest.py` for common setup
5. Follow the Arrange-Act-Assert pattern

Example:
```python
def test_feature_description(self, app):
    """Test that feature works as expected."""
    # Arrange
    setup_data = "test"
    
    # Act
    result = do_something(setup_data)
    
    # Assert
    assert result == expected_value
```
