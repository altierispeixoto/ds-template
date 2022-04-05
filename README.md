# 📑 DS Template

## Quick Start

```bash
# 👇 Install the template
pip install ds-template

# 🚀 Create a brand new project
putup --ds-template my_awesome_project

# 📦 Then, go to you project directory and update the dependencies
make update
```

## 4 Devs

If you are going to use Python Virtual Environment, follow the next steps.

```bash
# 👇 PyEnv
pyenv local 3.10.0

# 👇 Virtual Env.
python -m venv .venv \
  && source .venv/bin/activate \
  && python -m pip install --upgrade pip \
  && poetry install

# 👇 Pre Commit
pre-commit install &&
    pre-commit autoupdate &&
    pre-commit run -a -v
```

### How can I install this project while developing it?

```bash
pip install dist/ds-template-0.1.0.tar.gz
```

## References

For more information about PyScaffold and its extension mechanism, check out https://pyscaffold.org.

- Jupyter notebook: https://jupyter-notebook.readthedocs.io/
- flake8: https://flake8.pycqa.org/
- pre-commit: https://pre-commit.com/
- contribution guidelines: https://pyscaffold.org/en/latest/contributing.html
- pip: https://pip.pypa.io/en/stable/
- PyPI: https://pypi.org

[PEP 621 – Storing project metadata in pyproject.toml](https://peps.python.org/pep-0621/)
[PEP 518 – Specifying Minimum Build System Requirements for Python Projects](https://peps.python.org/pep-0518/)
[PEP 517 – A build-system independent format for source trees](https://peps.python.org/pep-0517/)
[The pyproject.toml file](https://python-poetry.org/docs/pyproject/)

