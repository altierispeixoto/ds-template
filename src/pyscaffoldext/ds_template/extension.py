"""Main logic to create custom extensions"""
import stat
from functools import partial, reduce
from typing import List

from packaging.version import Version
from pyscaffold import dependencies as deps
from pyscaffold.actions import Action, ActionParams, ScaffoldOpts, Structure
from pyscaffold.extensions import Extension, include
from pyscaffold.extensions.namespace import Namespace
from pyscaffold.extensions.no_skeleton import NoSkeleton
from pyscaffold.extensions.no_tox import NoTox
from pyscaffold.extensions.pre_commit import PreCommit
from pyscaffold.operations import add_permissions, no_overwrite, skip_on_update
from pyscaffold.log import logger
from pyscaffold.operations import no_overwrite
from pyscaffold.structure import (
    Leaf,
    ResolvedLeaf,
    merge,
    reify_content,
    reify_leaf,
    resolve_leaf,
)
from pyscaffold.templates import get_template, license

from pyscaffold.update import ConfigUpdater, pyscaffold_version

from . import templates


#PYSCAFFOLDEXT_NS = "pyscaffoldext"
EXTENSION_FILE_NAME = "extension"
NO_OVERWRITE = no_overwrite()
SKIP_ON_UPDATE = skip_on_update()
DOC_REQUIREMENTS = ["pyscaffold"]
TEST_DEPENDENCIES = (
    #"tox",
    "pre-commit",
    "setuptools_scm",
    "virtualenv",
    "configupdater",
    "pytest",
    "pytest-cov",
    "pytest-xdist",
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

    DEFAULT_MESSAGE = (
        "It's not possible to define a custom namespace "
        "when using ``--ds-template``."
    )

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
            action=include(NoSkeleton(), NoTox(), Namespace(), PreCommit(), self),
        )
        return self

    def activate(self, actions: List[Action]) -> List[Action]:
        """Activate extension, see :obj:`~pyscaffold.extension.Extension.activate`."""
        actions = self.register(actions, process_options, after="get_default_options")
        #actions = self.register(actions, add_doc_requirements)
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
        # Project configuration
        "pyproject.toml": (get_template("pyproject_toml"), NO_OVERWRITE),
        "setup.py": get_template("setup_py"),
        "setup.cfg": (get_template("setup_cfg"), NO_OVERWRITE),
        # Essential docs
        "README.md": (template("readme_md"), NO_OVERWRITE),
        "AUTHORS.rst": (get_template("authors"), NO_OVERWRITE),
        "LICENSE.txt": (license, NO_OVERWRITE),
        "CHANGELOG.rst": (get_template("changelog"), NO_OVERWRITE),
        "CONTRIBUTING.rst": (get_template("contributing"), NO_OVERWRITE),
        
        # Code
        "src": {
            opts["package"]: {
                "__init__.py": ("", NO_OVERWRITE),
                "skeleton.py": (get_template("skeleton"), SKIP_ON_UPDATE),
                "conftest.py": (template("conftest"), NO_OVERWRITE),
                "helpers.py": (template("helpers"), NO_OVERWRITE),
            }
        },
        "notebooks": {"template.ipynb": (template("template_ipynb"), NO_OVERWRITE)},
        "dags": {"my_dag.py": (template("my_dag_py"), NO_OVERWRITE)},
        "data": {
            ".gitignore": (template("gitignore_data"), NO_OVERWRITE),
            **{
                folder: {".gitignore": gitignore_all}
                for folder in ("external", "preprocessed", "raw")
            },
        },
        # Tests
        "tests": {
            "__init__.py": ("", NO_OVERWRITE),
            "conftest.py": (template("conftest"), NO_OVERWRITE),
            "helpers.py": (template("helpers"), NO_OVERWRITE),
            "conftest.py": (get_template("conftest_py"), NO_OVERWRITE),
            "test_skeleton.py": (get_template("test_skeleton"), SKIP_ON_UPDATE),
        }
    }

    return files, opts


def modify_setupcfg(definition: Leaf, opts: ScaffoldOpts) -> ResolvedLeaf:
    """Modify setup.cfg to add install_requires and pytest settings before it is
    written.
    See :obj:`pyscaffold.operations`.
    """
    contents, original_op = resolve_leaf(definition)

    if contents is None:
        raise ValueError("File contents for setup.cfg should not be None")

    setupcfg = ConfigUpdater()
    setupcfg.read_string(reify_content(contents, opts))

    modifiers = (add_pytest_requirements, add_entry_point)
    new_setupcfg = reduce(lambda acc, fn: fn(acc, opts), modifiers, setupcfg)

    return str(new_setupcfg), original_op


def add_entry_point(setupcfg: ConfigUpdater, opts: ScaffoldOpts) -> ConfigUpdater:
    """Adds the extension's entry_point to setup.cfg"""
    entry_points_key = "options.entry_points"

    if not setupcfg.has_section(entry_points_key):
        setupcfg["options"].add_after.section(entry_points_key)

    entry_points = setupcfg[entry_points_key]
    entry_points.insert_at(0).option("pyscaffold.cli")
    template = "{package} = {namespace}.{package}.{file_name}:{extension_class_name}"
    value = template.format(file_name=EXTENSION_FILE_NAME, **opts)
    entry_points["pyscaffold.cli"].set_values([value])

    return setupcfg


def add_pytest_requirements(setupcfg: ConfigUpdater, _opts) -> ConfigUpdater:
    """Add [options.extras_require] testing requirements for py.test"""
    extras_require = setupcfg["options.extras_require"]
    extras_require["testing"].set_values(TEST_DEPENDENCIES)
    return setupcfg


def add_doc_requirements(struct: Structure, opts: ScaffoldOpts) -> ActionParams:
    """In order to build the docs new requirements are necessary now.

    The default ``tox.ini`` generated by PyScaffold should already include
    ``-e {toxinidir}/docs/requirements.txt`` in its dependencies. Therefore,
    this action will make sure ``tox -e docs`` run without problems.

    It is important to sort the requirements otherwise pre-commit will raise an error
    for a newly generated file and that would correspond to a bad user experience.
    """
    leaf = struct.get("docs", {}).get("requirements.txt")
    original, file_op = reify_leaf(leaf, opts)
    contents = original or ""

    missing = [req for req in DOC_REQUIREMENTS if req not in contents]
    requirements = [*contents.splitlines(), *missing]

    # It is not trivial to sort the requirements because they include a comment header
    j = (i for (i, line) in enumerate(requirements) if line and not is_commented(line))
    comments_end = next(j, 0)  # first element of the iterator is a non commented line
    comments = requirements[:comments_end]
    sorted_requirements = sorted(requirements[comments_end:])

    new_contents = "\n".join([*comments, *sorted_requirements]) + "\n"
    # ^  pre-commit requires a new line at the end of the file

    files: Structure = {"docs": {"requirements.txt": (new_contents, file_op)}}

    return merge(struct, files), opts


def get_requirements() -> List[str]:
    """List of requirements for install_requires"""
    current_version = Version(pyscaffold_version)
    major, minor, *_ = current_version.base_version.split(".")
    next_major = int(major) + 1

    min_version = Version(f"{major}.{minor}")
    if current_version.is_prerelease:
        min_version = current_version

    return [f"pyscaffold>={min_version.public},<{next_major}.0a0"]


def is_commented(line):
    return line.strip().startswith("#")
