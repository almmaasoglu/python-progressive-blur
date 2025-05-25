# Contributing to Progressive Blur

Thank you for your interest in contributing to Progressive Blur! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Development Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/your-username/python-progressive-blur.git
   cd python-progressive-blur
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks**:
   ```bash
   pre-commit install
   ```

### Development Workflow

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards below

3. **Run tests**:
   ```bash
   pytest
   ```

4. **Run quality checks**:
   ```bash
   black progressive_blur tests examples
   isort progressive_blur tests examples
   flake8 progressive_blur tests
   mypy progressive_blur
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

6. **Push and create a pull request**:
   ```bash
   git push origin feature/your-feature-name
   ```

## 📝 Coding Standards

### Code Style

- **Formatting**: We use [Black](https://black.readthedocs.io/) for code formatting
- **Import sorting**: We use [isort](https://pycqa.github.io/isort/) with Black profile
- **Linting**: We use [flake8](https://flake8.pycqa.org/) for linting
- **Type hints**: All public functions must have type hints
- **Docstrings**: All public functions must have comprehensive docstrings

### Code Quality

- **Line length**: Maximum 88 characters (Black default)
- **Type hints**: Use type hints for all function parameters and return values
- **Error handling**: Provide meaningful error messages and handle edge cases
- **Performance**: Consider performance implications, especially for image processing

### Documentation

- **Docstrings**: Use Google-style docstrings
- **Comments**: Write clear, concise comments for complex logic
- **Examples**: Include usage examples in docstrings where appropriate

Example docstring:
```python
def apply_progressive_blur(
    image: ImageInput,
    max_blur: float = 50.0,
    direction: Union[BlurDirection, str] = BlurDirection.TOP_TO_BOTTOM,
) -> Image.Image:
    """
    Apply a progressive blur effect to an image.
    
    Args:
        image: Input image (PIL.Image, bytes, or file path)
        max_blur: Maximum blur radius in pixels
        direction: Direction of the blur effect
        
    Returns:
        PIL.Image: The processed image with progressive blur effect
        
    Raises:
        ValueError: If max_blur is not positive
        TypeError: If image input type is not supported
        
    Example:
        >>> from PIL import Image
        >>> img = Image.open("photo.jpg")
        >>> blurred = apply_progressive_blur(img, max_blur=30.0)
        >>> blurred.save("blurred_photo.jpg")
    """
```

## 🧪 Testing

### Writing Tests

- **Coverage**: Aim for high test coverage (>90%)
- **Test types**: Write unit tests for individual functions and integration tests for workflows
- **Test data**: Use small, synthetic test images to keep tests fast
- **Edge cases**: Test boundary conditions and error cases

### Test Structure

```python
class TestYourFeature:
    """Test your feature functionality."""
    
    def test_basic_functionality(self):
        """Test basic usage."""
        # Arrange
        img = Image.new('RGB', (100, 100), color='red')
        
        # Act
        result = your_function(img)
        
        # Assert
        assert isinstance(result, Image.Image)
        assert result.size == img.size
    
    def test_edge_case(self):
        """Test edge case handling."""
        with pytest.raises(ValueError, match="Expected error message"):
            your_function(invalid_input)
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=progressive_blur --cov-report=html

# Run specific test file
pytest tests/test_core.py

# Run specific test
pytest tests/test_core.py::TestProgressiveBlur::test_basic_blur
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment information**:
   - Python version
   - Operating system
   - Package version
   - Dependencies versions

2. **Reproduction steps**:
   - Minimal code example
   - Input data (if possible)
   - Expected vs. actual behavior

3. **Error messages**:
   - Full traceback
   - Any relevant log output

## ✨ Feature Requests

When requesting features:

1. **Use case**: Describe the problem you're trying to solve
2. **Proposed solution**: Suggest how the feature might work
3. **Alternatives**: Mention any workarounds you've considered
4. **Examples**: Provide code examples of how you'd like to use the feature

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (if applicable)
- [ ] Type hints are added
- [ ] Docstrings are comprehensive

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing performed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

## 🏗️ Architecture Guidelines

### Package Structure

```
progressive_blur/
├── __init__.py          # Public API exports
├── core.py              # Core blur algorithms
├── utils.py             # Utility functions
├── cli.py               # Command-line interface
└── types.py             # Type definitions (if needed)
```

### Design Principles

1. **Modularity**: Keep functions focused and composable
2. **Performance**: Optimize for common use cases
3. **Usability**: Provide sensible defaults and clear error messages
4. **Extensibility**: Design for easy addition of new algorithms and features
5. **Backward compatibility**: Avoid breaking changes when possible

### Adding New Features

When adding new features:

1. **Core functionality** goes in `core.py`
2. **Utility functions** go in `utils.py`
3. **CLI commands** go in `cli.py`
4. **Update exports** in `__init__.py`
5. **Add tests** in appropriate test files
6. **Update documentation** in README.md

## 🔄 Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] Update version in `pyproject.toml`
- [ ] Update `CHANGELOG.md`
- [ ] Run full test suite
- [ ] Update documentation
- [ ] Create release tag
- [ ] Publish to PyPI

## 🤝 Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn and grow
- Focus on the technical merits

### Communication

- **Issues**: For bug reports and feature requests
- **Discussions**: For questions and general discussion
- **Pull Requests**: For code contributions

## 📚 Resources

### Documentation
- [PIL/Pillow Documentation](https://pillow.readthedocs.io/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

### Tools
- [Black Code Formatter](https://black.readthedocs.io/)
- [isort Import Sorter](https://pycqa.github.io/isort/)
- [pytest Testing Framework](https://docs.pytest.org/)
- [mypy Type Checker](https://mypy.readthedocs.io/)

## ❓ Questions?

If you have questions about contributing:

1. Check existing [issues](https://github.com/almmaasoglu/python-progressive-blur/issues)
2. Start a [discussion](https://github.com/almmaasoglu/python-progressive-blur/discussions)
3. Reach out to maintainers

Thank you for contributing to Progressive Blur! 🎉 