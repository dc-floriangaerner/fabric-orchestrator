# Contributing to Fabric Orchestrator

Thank you for your interest in contributing to Fabric Orchestrator!

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/your-username/fabric-orchestrator.git
cd fabric-orchestrator
```

2. Install development dependencies:
```bash
pip install -e ".[dev]"
```

3. Run tests to verify setup:
```bash
pytest
```

## Development Workflow

1. Create a feature branch:
```bash
git checkout -b feature/my-feature
```

2. Make your changes and add tests

3. Run code quality checks:
```bash
# Format code
ruff format .

# Lint code
ruff check .

# Type check
mypy src/fabric_orchestrator

# Run tests
pytest --cov=fabric_orchestrator
```

4. Commit your changes:
```bash
git commit -m "Add my feature"
```

5. Push and create a pull request:
```bash
git push origin feature/my-feature
```

## Code Style

- Follow PEP 8 style guide
- Use type hints for all functions
- Write docstrings for all public APIs
- Keep line length to 120 characters
- Use double quotes for strings

## Testing

- Write tests for all new features
- Maintain or improve code coverage
- Run the full test suite before submitting PR

## Pull Request Process

1. Update README.md with any new features
2. Add tests for new functionality
3. Ensure all tests pass
4. Update version number if needed
5. Request review from maintainers

## Questions?

Open an issue or discussion on GitHub.
