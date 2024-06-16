# 📑 Data Science Template

## Quick Start

```bash
# 👇 Install the template
pip install ds-template

# 🚀 Create a brand new project
putup --ds-template my_awesome_project

```

## How to use

```bash

conda create --prefix .venv python=3.10
conda activate ./.env

conda install conda-forge::poetry==1.8.3

poetry install
# 👇 Pre Commit
pre-commit install &&
    pre-commit autoupdate &&
    pre-commit run -a -v
```

### How can I install this project while developing it?

```bash
poetry build
pip install dist/ds-template-0.1.0.tar.gz
```
