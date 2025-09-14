# Data Science Template Generator 

[![License](https://img.shields.io/github/license/altierispeixoto/ds-template)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](pyproject.toml)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

A professional Data Science project template generator that sets up a standardized, production-ready project structure with best practices in mind.

## 🌟 Features

- ✨ Modern Python project structure
- 🐳 Docker containerization
- 📊 Data versioning with DVC
- 🔍 Code quality tools (Ruff, pre-commit)
- 📓 Jupyter notebook templates
- 🗃️ Organized data directory structure
- 🧪 Testing framework setup
- 🔒 Environment management
- 📝 SQL linting configuration

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- uv package manager (`pip install uv`)

### Installation

```bash
uv pip install git+ssh://git@github.com/altierispeixoto/ds-template.git
```

### Create a New Project

```bash
putup --ds-template my_awesome_project
```

## 📁 Project Structure

The generated project follows a well-organized structure:
```
.
├── .dockerignore
├── .env-template
├── .git
├── .gitignore
├── .pre-commit-config.yaml
├── CHANGELOG.rst
├── CONTRIBUTING.rst
├── Dockerfile
├── README.md
├── data
│   ├── .gitignore
│   ├── model_features
│   ├── processed
│   ├── raw
│   └── staging
├── justfile
├── notebooks
│   └── template.ipynb
├── pyproject.toml
├── ruff.toml
├── sql
│   └── .sqlfluff
├── src
│   └── my_awesome_project
└── tests
    ├── __init__.py
    └── test_my_module.py
```

## 🛠️ Technologies Used

| Technology                            | Purpose                                    |
| ------------------------------------- | ------------------------------------------ |
| [uv](https://github.com/astral-sh/uv) | Fast Python package installer and resolver |
| [Docker](https://www.docker.com/)     | Application containerization               |
| [DVC](https://dvc.org/)               | Data & model versioning                    |
| [Ruff](https://beta.ruff.rs/docs/)    | Fast Python linter & formatter             |
| [Pre-commit](https://pre-commit.com/) | Git hooks for code quality                 |

## 🏁 Getting Started

1. Generate your project:
   ```bash
   putup --ds-template my_awesome_project
   cd my_awesome_project
   ```

2. Initialize git repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <your-repository-url>
   git push -u origin main
   ```

3. Set up your environment:
   ```bash
   # Copy environment template
   cp .env-template .env
   
   # Edit .env with your configurations
   ```

## 📚 Documentation

- See [CONTRIBUTING.rst](CONTRIBUTING.rst) for development guidelines
- Check [CHANGELOG.rst](CHANGELOG.rst) for version history
- Review [justfile](justfile) for common commands

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by best practices from the data science community
- Built with modern Python tooling
- Designed for scalability and reproducibility