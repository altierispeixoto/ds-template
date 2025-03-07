# Set the Python version
python_version := "3.12"

# Default recipe to display available commands
default:
    @just --list

# Create a virtual environment using uv with specified Python version and set up pre-commit
setup:
    @echo "Creating virtual environment using Python {{python_version}}..."
    uv venv --python {{python_version}}
    @echo "Virtual environment created."
    @echo "Installing pre-commit hooks..."
    @just run uv sync
    @just run pre-commit install && pre-commit autoupdate && pre-commit run -a -v
    @echo "Pre-commit hooks installed."
    @echo "To activate the environment, run: just activate"


# Run a command in the virtual environment
run *ARGS:
    @if [ ! -d ".venv" ]; then \
        echo "Virtual environment not found. Creating one..."; \
        uv venv --python {{python_version}}; \
    fi
    @source .venv/bin/activate && {{ ARGS }}

# Activate the virtual environment
activate:
    #!/usr/bin/env bash
    source .venv/bin/activate
    echo "Virtual environment activated. Run 'deactivate' to exit."
    $SHELL

# Deactivate the virtual environment
deactivate:
    @echo "To deactivate the virtual environment, simply run 'deactivate' in your shell."
    @echo "If you're in a subshell created by 'just activate', type 'exit' to leave it."


# Install project dependencies using uv sync
install:
    @echo "Installing project dependencies..."
    @just run uv sync

# Update project dependencies using uv sync with upgrade
update:
    @echo "Updating project dependencies..."
    @just run uv sync --upgrade

# Clean up the virtual environment
clean:
    @echo "Removing virtual environment..."
    rm -rf .venv
    @echo "Virtual environment removed."
