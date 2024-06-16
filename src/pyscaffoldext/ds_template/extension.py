"""Main logic to create custom extensions"""

from functools import partial
from typing import List

from packaging.version import Version
from pyscaffold import dependencies as deps
from pyscaffold.actions import Action, ActionParams, ScaffoldOpts, Structure
from pyscaffold.extensions import Extension, include
from pyscaffold.extensions.no_skeleton import NoSkeleton
from pyscaffold.operations import no_overwrite, skip_on_update
from pyscaffold.templates import get_template, license
from pyscaffold.update import pyscaffold_version

from . import templates

EXTENSION_FILE_NAME = "extension"
NO_OVERWRITE = no_overwrite()
SKIP_ON_UPDATE = skip_on_update()
DOC_REQUIREMENTS = ["pyscaffold"]
TEST_DEPENDENCIES = (
    "pre-commit",
    "pytest",
    "pytest-cov",
)

INVALID_PROJECT_NAME = (
    "The prefix ``pyscaffoldext-`` will be added to the package name "
    "(as in PyPI/pip install). "
    "If that is not your intention, please use ``--force`` to overwrite."
)
"""Project name does not comply with convention of an extension"""


template = partial(get_template, relative_to=templates)


class NamespaceError(RuntimeError):
    """No additional namespace is allowed"""

    DEFAULT_MESSAGE = "It's not possible to define a custom namespace " "when using ``--ds-template``."

    def __init__(self, message=DEFAULT_MESSAGE, *args, **kwargs):
        super().__init__(message, *args, **kwargs)


class CustomExtension(Extension):
    """Configures a project to start creating extensions"""

    def augment_cli(self, parser):
        """Augments the command-line interface parser

        A command line argument ``--FLAG`` where FLAG=``self.name`` is added
        which appends ``self.activate`` to the list of extensions. As help
        text the docstring of the extension class is used.
        In most cases this method does not need to be overwritten.

        Args:
            parser: current parser object
        """

        parser.add_argument(
            self.flag,
            help=self.help_text,
            nargs=0,
            action=include(NoSkeleton(), self),  # NoTox() Namespace(), PreCommit()
        )
        return self

    def activate(self, actions: List[Action]) -> List[Action]:
        """Activate extension, see :obj:`~pyscaffold.extension.Extension.activate`."""
        actions = self.register(actions, process_options, after="get_default_options")
        actions = self.register(actions, add_files)
        return actions


def process_options(struct: Structure, opts: ScaffoldOpts) -> ActionParams:
    """Process the given options enforcing policies and calculating derived ones.

    Policies:

    - Fixed ``namespace`` value of pyscaffoldext (and no extra namespace)
    - The project name must start with ``pyscaffoldext-``.
    - The package name shouldn't contain the redundant ``pyscaffoldext_`` in the
      beginning of the name.

    See :obj:`pyscaffold.actions.Action`.
    """
    opts = opts.copy()

    opts["requirements"] = deps.add(opts.get("requirements", []), get_requirements())

    # set another derived parameter used in the templates
    class_name = "".join(map(str.capitalize, opts["package"].split("_")))
    return struct, {**opts, "extension_class_name": class_name}


def add_files(struct: Structure, opts: ScaffoldOpts) -> ActionParams:
    """Add custom extension files. See :obj:`pyscaffold.actions.Action`"""

    gitignore_all = (template("gitignore_all"), NO_OVERWRITE)

    files: Structure = {
        # Tools
        ".gitignore": (get_template("gitignore"), NO_OVERWRITE),
        ".flake8": (template("flake8"), NO_OVERWRITE),
        ".env-template": (template("env"), NO_OVERWRITE),
        # Project configuration
        "pyproject.toml": (template("pyproject_toml"), NO_OVERWRITE),
        # Essential docs
        "README.md": (template("readme_md"), NO_OVERWRITE),
        "AUTHORS.rst": (get_template("authors"), NO_OVERWRITE),
        "LICENSE.txt": (license, NO_OVERWRITE),
        "CHANGELOG.rst": (get_template("changelog"), NO_OVERWRITE),
        "CONTRIBUTING.rst": (get_template("contributing"), NO_OVERWRITE),
        # Code
        "src": {opts["package"]: {"__init__.py": ("", NO_OVERWRITE)}},
        "notebooks": {"template.ipynb": (template("template_ipynb"), NO_OVERWRITE)},
        "data": {
            ".gitignore": (template("gitignore_data"), NO_OVERWRITE),
            **{
                folder: {".gitignore": gitignore_all}
                for folder in ("staging", "raw", "model_features", "processed")
            },
        },
        # Tests
        "tests": {
            "__init__.py": ("", NO_OVERWRITE),
        },
        ".pre-commit-config.yaml": (template("pre-commit-config"), NO_OVERWRITE),
    }

    return files, opts


def get_requirements() -> List[str]:
    """List of requirements for install_requires"""
    current_version = Version(pyscaffold_version)
    major, minor, *_ = current_version.base_version.split(".")
    next_major = int(major) + 1

    min_version = Version(f"{major}.{minor}")
    if current_version.is_prerelease:
        min_version = current_version

    return [f"pyscaffold>={min_version.public},<{next_major}.0a0"]
