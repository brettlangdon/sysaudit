import unittest

import pytest

import sysaudit


def hook(event, args):
    pass


@pytest.mark.benchmark(group="audit")
def test_csysaudit_audit(benchmark):
    sysaudit.csysaudit_addaudithook(hook)

    benchmark(sysaudit.csysaudit_audit, "event", 1, 2, 3)


@pytest.mark.benchmark(group="audit")
def test_std_audit(benchmark):
    if not sysaudit.std_audit:
        raise unittest.SkipTest("stdlib version not available")

    sysaudit.std_addaudithook(hook)
    benchmark(sysaudit.std_audit, "event", 1, 2, 3)


@pytest.mark.benchmark(group="audit")
def test_py_audit(benchmark):
    sysaudit.py_addaudithook(hook)
    benchmark(sysaudit.py_audit, "event", 1, 2, 3)
