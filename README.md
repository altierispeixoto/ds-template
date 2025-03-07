# 📑 Data Science Template Generator

## Quick Start

```bash
# 👇 Install the template
pip install git+ssh://git@github.com/altierispeixoto/ds-template.git

# 🚀 Create a brand new project
putup --ds-template my_awesome_project

```

This will create a new directory with the following structure:
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

## The project created uses:
[uv](https://github.com/astral-sh/uv) to manage python packages.  
[Docker](https://www.docker.com/) is used to containerize the application.  
[DVC](https://dvc.org/) is used to version the data and models.  
[Ruff](https://beta.ruff.rs/docs/configuration/) is used to lint the code.  
[Pre-commit](https://pre-commit.com/) is used to run all pre-commit hooks, linting and formatting, cleaning notebooks and more.   


## To add the new project to git basically refer the remote repository and push the code

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-repository-url>

```