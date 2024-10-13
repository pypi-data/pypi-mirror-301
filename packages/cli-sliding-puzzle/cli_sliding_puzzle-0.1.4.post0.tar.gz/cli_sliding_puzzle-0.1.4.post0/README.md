# CLI Sliding Puzzle Game

A command-line interface sliding puzzle game built with Python.

## Installation

To install the game, you need Python 3.7 or higher and pip. Then run:

pip install cli-sliding-puzzle

## Playing the Game

After installation, run the game by typing:

sliding-puzzle

Use arrow keys to move tiles. Press 'q' to quit.

## Development

### Setup

1. Clone the repository:
   git clone https://github.com/yourusername/cli-sliding-puzzle.git
   cd cli-sliding-puzzle

2. Create a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install development dependencies:
   pip install build twine setuptools_scm

### Building and Publishing

1. Ensure all changes are committed to git.

2. List existing tags to determine the next version number:
   ```bash
   git tag --list
   ```

3. Create a new git tag for the version:
   ```bash
   git tag -a vX.X.X -m "Release version X.X.X"
   git push origin vX.X.X
   ```

4. Clean up the dist directory:
   ```bash
   rm -rf dist/*
   ```

5. Build the package:
   ```bash
   python -m build
   ```

6. Test the package locally:
   ```bash
   # List the contents of the dist directory
   ls dist/
   
   # Install the latest version (replace X.X.X with the latest version number you see)
   pip install dist/cli_sliding_puzzle-X.X.X-py3-none-any.whl
   ```

7. Upload to TestPyPI:
   ```bash
   twine upload --repository testpypi dist/*
   ```

8. Test the TestPyPI upload:
   ```bash
   # Create a new virtual environment for testing
   python -m venv test_venv
   source test_venv/bin/activate  # On Windows, use `test_venv\Scripts\activate`

   # Install the package from TestPyPI
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple cli-sliding-puzzle

   # Test the installed package
   sliding-puzzle

   # Deactivate the test environment when done
   deactivate
   ```

9. If everything works, upload to PyPI:
   ```bash
   twine upload dist/*
   ```

## License

This project is licensed under the MIT License.
