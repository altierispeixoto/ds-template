# 📑 DS Template

## Quick Start

```bash
# 👇 Install the template
pip install ds-template

# 🚀 Create a brand new project
putup --ds-template my_awesome_project
```

## 4 Devs

If you are going to use Python Virtual Environment, follow the next steps.

```bash
# 👇 PyEnv
pyenv local 3.10.0

# 👇 Virtual Env.
python -m venv .venv \
  && source .venv/bin/activate \
  && python -m pip install --upgrade pip

# 👇 Pre Commit
pip install pre-commit
pre-commit install &&
    pre-commit autoupdate &&
    pre-commit run -a -v
```

### How can I install this project while developing it?

```bash
pip install -e
```

## References

For more information about PyScaffold and its extension mechanism, check out https://pyscaffold.org.

- Jupyter notebook: https://jupyter-notebook.readthedocs.io/
- flake8: https://flake8.pycqa.org/
- pre-commit: https://pre-commit.com/
- contribution guidelines: https://pyscaffold.org/en/latest/contributing.html
- pip: https://pip.pypa.io/en/stable/
- PyPI: https://pypi.org
