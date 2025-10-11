# Contributing to Com-Tech

Thank you for your interest in contributing to Com-Tech! We welcome contributions from the community and are grateful for any help you can provide.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment. Please:

- Be respectful and considerate of others
- Welcome newcomers and help them get started
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Com-tech3.git
   cd Com-tech3
   ```
3. **Set up the development environment** following the instructions in [README.md](README.md)
4. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## How to Contribute

There are many ways to contribute to Com-Tech:

- **Fix bugs**: Check the issue tracker for bugs to fix
- **Add features**: Implement new features or improvements
- **Improve documentation**: Help make our docs clearer and more comprehensive
- **Write tests**: Increase test coverage for existing code
- **Review code**: Review pull requests from other contributors
- **Report bugs**: Submit detailed bug reports
- **Suggest features**: Propose new features or enhancements

## Development Workflow

1. **Check existing issues** to see if your contribution is already being worked on
2. **Create an issue** if one doesn't exist for your contribution
3. **Discuss your approach** in the issue before starting major work
4. **Write code** following our coding standards
5. **Add tests** for any new functionality
6. **Update documentation** as needed
7. **Submit a pull request** when ready

## Coding Standards

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines
- Use meaningful variable and function names
- Write docstrings for functions and classes
- Keep functions small and focused
- Use type hints where appropriate

Example:
```python
def calculate_user_score(user_id: int, include_bonus: bool = False) -> float:
    """
    Calculate the total score for a user.
    
    Args:
        user_id: The ID of the user
        include_bonus: Whether to include bonus points
        
    Returns:
        The calculated score as a float
    """
    # Implementation here
    pass
```

### Frontend Code Style

- Use consistent indentation (2 spaces for HTML/CSS/JS)
- Write semantic HTML
- Follow modern JavaScript best practices
- Keep CSS organized and use classes over IDs when possible

### Database Models

- Use descriptive table and column names
- Include proper indexes for performance
- Document relationships clearly
- Add appropriate constraints and validations

## Testing Guidelines

### Writing Tests

- Write tests for all new features and bug fixes
- Aim for high test coverage (>80%)
- Use descriptive test names that explain what is being tested
- Follow the Arrange-Act-Assert pattern

Example:
```python
def test_user_registration_creates_new_user():
    """Test that user registration creates a new user in the database."""
    # Arrange
    user_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@example.com',
        'password': 'secure_password'
    }
    
    # Act
    response = client.post('/auth/register', data=user_data)
    user = User.query.filter_by(email='john@example.com').first()
    
    # Assert
    assert response.status_code == 302  # Redirect after success
    assert user is not None
    assert user.first_name == 'John'
```

### Running Tests

Before submitting a pull request:

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_models.py

# Run tests matching a pattern
pytest -k "test_user"
```

## Submitting Changes

### Pull Request Process

1. **Update your branch** with the latest main branch:
   ```bash
   git checkout main
   git pull upstream main
   git checkout your-branch
   git rebase main
   ```

2. **Ensure all tests pass**:
   ```bash
   pytest
   ```

3. **Commit your changes** with clear, descriptive messages:
   ```bash
   git commit -m "Add user profile editing feature"
   ```

4. **Push to your fork**:
   ```bash
   git push origin your-branch
   ```

5. **Create a Pull Request** on GitHub with:
   - A clear title describing the change
   - A detailed description of what was changed and why
   - References to related issues (e.g., "Fixes #123")
   - Screenshots for UI changes

### Commit Message Guidelines

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Examples:
```
Add user profile editing functionality

- Created new profile edit route
- Added form validation for profile updates
- Updated user model to support profile changes

Fixes #123
```

## Reporting Bugs

When reporting bugs, please include:

- **Clear title**: Descriptive summary of the issue
- **Environment**: OS, Python version, browser (if applicable)
- **Steps to reproduce**: Detailed steps to reproduce the bug
- **Expected behavior**: What you expected to happen
- **Actual behavior**: What actually happened
- **Screenshots**: If applicable
- **Error messages**: Full error messages and stack traces
- **Additional context**: Any other relevant information

## Suggesting Features

When suggesting features, please:

1. **Check existing issues** to avoid duplicates
2. **Describe the feature** clearly and in detail
3. **Explain the use case** - why is this feature needed?
4. **Provide examples** of how it would work
5. **Consider alternatives** - are there other ways to solve the problem?

## Questions?

If you have questions about contributing, feel free to:

- Open an issue with the "question" label
- Reach out to the maintainers
- Check existing documentation and issues

## Recognition

Contributors will be recognized in the project's README and release notes. Thank you for helping make Com-Tech better!
