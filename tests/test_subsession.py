import sys

import pytest

from pytest_isolate_mpi._subsession import assemble_sub_pytest_cmd


@pytest.mark.parametrize(
    ["options", "expected_subsession_cmd"],
    [
        pytest.param(
            ["foo"],
            [
                sys.executable,
                "-m",
                "mpi4py",
                "-m",
                "pytest",
                "--capture",
                "fd",
                "--no-header",
                "--no-summary",
                "--tb",
                "auto",
                "--show-capture",
                "all",
                "--color",
                "auto",
                "--code-highlight",
                "yes",
                "--import-mode",
                "prepend",
                "test_foo.py::test_bar",
            ],
            id="no_options",
        ),
        pytest.param(
            ["-s", "--runxfail"],
            [
                sys.executable,
                "-m",
                "mpi4py",
                "-m",
                "pytest",
                "--capture",
                "no",
                "--runxfail",
                "--no-header",
                "--no-summary",
                "--tb",
                "auto",
                "--show-capture",
                "all",
                "--color",
                "auto",
                "--code-highlight",
                "yes",
                "--import-mode",
                "prepend",
                "test_foo.py::test_bar",
            ],
            id="general",
        ),
        pytest.param(
            [
                "-vvv",
                "--disable-warnings",
                "--showlocals",
                "--tb",
                "no",
                "--show-capture",
                "no",
                "--full-trace",
                "--color",
                "yes",
                "--code-highlight",
                "no",
            ],
            [
                sys.executable,
                "-m",
                "mpi4py",
                "-m",
                "pytest",
                "--capture",
                "fd",
                "--no-header",
                "--no-summary",
                "-vvv",
                "--disable-warnings",
                "--showlocals",
                "--tb",
                "no",
                "--show-capture",
                "no",
                "--full-trace",
                "--color",
                "yes",
                "--code-highlight",
                "no",
                "--import-mode",
                "prepend",
                "test_foo.py::test_bar",
            ],
            id="reporting",
        ),
        pytest.param(
            ["-W", "a", "-c", "foo.ini"],
            [
                sys.executable,
                "-m",
                "mpi4py",
                "-m",
                "pytest",
                "--capture",
                "fd",
                "--no-header",
                "--no-summary",
                "--tb",
                "auto",
                "--show-capture",
                "all",
                "--color",
                "auto",
                "--code-highlight",
                "yes",
                "--pythonwarnings",
                "a",
                "--config-file",
                "foo.ini",
                "--import-mode",
                "prepend",
                "test_foo.py::test_bar",
            ],
            id="pytest_warnings",
        ),
        pytest.param(
            ["--confcutdir", ".", "--noconftest"],
            [
                sys.executable,
                "-m",
                "mpi4py",
                "-m",
                "pytest",
                "--capture",
                "fd",
                "--no-header",
                "--no-summary",
                "--tb",
                "auto",
                "--show-capture",
                "all",
                "--color",
                "auto",
                "--code-highlight",
                "yes",
                "--confcutdir",
                ".",
                "--noconftest",
                "--import-mode",
                "prepend",
                "test_foo.py::test_bar",
            ],
            id="collection",
        ),
        pytest.param(
            [
                "--basetemp",
                "/tmp",
                "-p",
                "isolate-mpi",
                "--trace-config",
                "--override-ini",
                "xfail_strict=True",
                "--assert",
                "plain",
                "--setup-only",
                "--setup-show",
                "--setup-plan",
            ],
            [
                sys.executable,
                "-m",
                "mpi4py",
                "-m",
                "pytest",
                "--capture",
                "fd",
                "--no-header",
                "--no-summary",
                "--tb",
                "auto",
                "--show-capture",
                "all",
                "--color",
                "auto",
                "--code-highlight",
                "yes",
                "--import-mode",
                "prepend",
                "-p",
                "isolate-mpi",
                "--trace-config",
                "--override-ini",
                "xfail_strict=True",
                "--assert",
                "plain",
                "--setup-only",
                "--setup-show",
                "--setup-plan",
                "test_foo.py::test_bar",
            ],
            id="test_session",
        ),
        pytest.param(
            [
                "--log-level",
                "DEBUG",
                "--log-format",
                "%(message)s",
                "--log-date-format",
                "%H:%M:%S",
                "--log-cli-level",
                "DEBUG",
                "--log-cli-format",
                "%(message)s",
                "--log-cli-date-format",
                "%H:%M:%S",
                "--log-file-level",
                "DEBUG",
                "--log-file-format",
                "%(message)s",
                "--log-file-date-format",
                "%H:%M:%S",
                "--log-auto-indent",
                "2",
                "--log-disable",
                "foo",
            ],
            [
                sys.executable,
                "-m",
                "mpi4py",
                "-m",
                "pytest",
                "--capture",
                "fd",
                "--no-header",
                "--no-summary",
                "--tb",
                "auto",
                "--show-capture",
                "all",
                "--color",
                "auto",
                "--code-highlight",
                "yes",
                "--import-mode",
                "prepend",
                "--log-level",
                "DEBUG",
                "--log-format",
                "%(message)s",
                "--log-cli-level",
                "DEBUG",
                "--log-cli-format",
                "%(message)s",
                "--log-cli-date-format",
                "%H:%M:%S",
                "--log-file-level",
                "DEBUG",
                "--log-file-format",
                "%(message)s",
                "--log-file-date-format",
                "%H:%M:%S",
                "--log-auto-indent",
                "2",
                "--log-disable",
                "foo",
                "test_foo.py::test_bar",
            ],
            id="logging",
        ),
    ],
)
def test_assemble_sub_pytest_cmd(pytestconfig, options, expected_subsession_cmd):
    parser = pytestconfig._parser  # pylint: disable=protected-access
    options = parser.parse(options)
    cmd = assemble_sub_pytest_cmd(options, "test_foo.py::test_bar")
    assert cmd == expected_subsession_cmd