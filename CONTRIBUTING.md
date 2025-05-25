# Contributing to Progressive Blur

Hey there! Thanks for considering contributing to Progressive Blur! We're excited to have you here. 🎉

## Getting Started

### Setting Up Your Dev Environment

1. **Fork and clone the repo**:
   ```bash
   git clone https://github.com/your-username/python-progressive-blur.git
   cd python-progressive-blur
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the package in dev mode**:
   ```bash
   pip install -e ".[dev]"
   ```

That's it! You're ready to start contributing.

## Making Changes

### Quick Workflow

1. Create a new branch: `git checkout -b my-cool-feature`
2. Make your changes
3. Run tests: `pytest`
4. Push and create a PR!

### Code Style

We use a few tools to keep the code consistent, but don't worry - they're mostly automatic:

- **Black** for formatting (just run `black .`)
- **Type hints** where they make sense (but don't stress about it)

## Testing

If you're adding new features, it'd be great if you could add some tests. Look at the existing tests in `tests/` for examples. Run tests with:

```bash
pytest
```

## Submitting a Pull Request

1. Push your changes to your fork
2. Create a Pull Request
3. Describe what you changed and why
4. That's it! We'll review it and work with you to get it merged

## Types of Contributions We Love

- 🐛 **Bug fixes** - Found something broken? Fix it!
- ✨ **New features** - Have an idea? Let's discuss it!
- 📝 **Documentation** - Help others understand how to use the library
- 🎨 **Examples** - Show cool ways to use progressive blur
- 💡 **Ideas** - Even if you can't code it, share your thoughts!

## Questions?

Feel free to:
- Open an issue to discuss your idea
- Ask questions in discussions
- Reach out if you need help

## Code Style Guide (The Basics)

### Python Style

```python
# We like clear variable names
blur_radius = 50.0  # Good
br = 50.0  # Less clear

# Add docstrings to help others understand
def apply_blur(image, radius):
    """Apply blur effect to an image."""
    # Your code here
```

### Commit Messages

Keep them simple and clear:
- `fix: correct blur calculation for RGBA images`
- `feat: add motion blur algorithm`
- `docs: update README examples`

## Running Quality Checks

If you want to run the same checks we do:

```bash
# Format code
black progressive_blur tests examples

# Run tests
pytest

# Check types (optional)
mypy progressive_blur
```

## Don't Worry About Being Perfect

- **Your first PR doesn't need to be perfect** - We'll help you improve it
- **Ask questions** - We're here to help
- **Small contributions are welcome** - Even fixing a typo helps!

## Community

We're building a friendly community around this project. Everyone is welcome, regardless of experience level. If you're new to open source, this is a great place to start!

Remember: **There are no stupid questions!** We all started somewhere.

Thanks again for contributing! We're looking forward to seeing what you create. 🚀 