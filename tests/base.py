import subprocess
import sys
import unittest

if sys.version_info < (3, 8):
    IMPLEMENTATIONS = ("csysaudit", "pysysaudit")
else:
    IMPLEMENTATIONS = ("stdlib", "csysaudit", "pysysaudit")


class BaseTest(unittest.TestCase):
    TEST_FILE_PY = None  # type: str

    def _do_test(self, *args, **kwargs):
        popen_kwargs = dict(
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if "impl" in kwargs:
            popen_kwargs["env"] = dict(SYSAUDIT_IMPL=kwargs["impl"])
        if sys.version_info >= (3, 6):
            popen_kwargs["encoding"] = "utf-8"

        p = subprocess.Popen(
            [sys.executable, self.TEST_FILE_PY] + list(args), **popen_kwargs
        )
        p.wait()
        sys.stdout.writelines(p.stdout)
        sys.stderr.writelines(p.stderr)
        if p.returncode:
            self.fail("".join(p.stderr))

    def do_test(self, *args):
        for impl in IMPLEMENTATIONS:
            return self._do_test(*args, impl=impl)

    def _run_python(self, *args, **kwargs):
        events = []

        popen_kwargs = dict(
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if "impl" in kwargs:
            popen_kwargs["env"] = dict(SYSAUDIT_IMPL=kwargs["impl"])
        if sys.version_info >= (3, 6):
            popen_kwargs["encoding"] = "utf-8"

        p = subprocess.Popen(
            [sys.executable, self.TEST_FILE_PY] + list(args), **popen_kwargs
        )
        p.wait()
        sys.stderr.writelines(p.stderr)
        return (
            p.returncode,
            [line.strip().partition(" ") for line in p.stdout],
            "".join(p.stderr),
        )

    def run_python(self, *args):
        for impl in IMPLEMENTATIONS:
            return self._run_python(*args, impl=impl)
