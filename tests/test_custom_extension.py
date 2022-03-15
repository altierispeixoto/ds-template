from pathlib import Path

import pytest
from pyscaffold import cli

from pyscaffoldext.custom_extension.extension import NamespaceError


def test_add_custom_extension(tmpfolder):
    args = [
        "pyscaffoldext-my_project",
        "--no-config",  # <- Avoid extra config from dev's machine interference
        "--ds-template",
        "--package",
        "my_extension",
    ]
    cli.main(args)
    extension = "pyscaffoldext-my_project/src/pyscaffoldext/my_extension/extension.py"
    assert Path(extension).exists()


def test_add_custom_extension_and_pretend(tmpfolder):
    args = [
        "pyscaffoldext-my_project",
        "--no-config",  # <- Avoid extra config from dev's machine interference
        "--pretend",
        "--ds-template",
        "--package",
        "my_extension",
    ]
    cli.main(args)
    assert not Path("pyscaffoldext-my_project").exists()


def test_add_custom_extension_with_namespace(tmpfolder):
    # We expect the second namespace to be just ignored
    args = [
        "--no-config",  # <- Avoid extra config from dev's machine interference
        "--namespace",
        "test",
        "--ds-template",
        "pyscaffoldext-some_extension",
    ]
    with pytest.raises(NamespaceError):
        cli.main(args)
