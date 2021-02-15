import subprocess
import sys
import unittest


class BaseTest(unittest.TestCase):
    TEST_FILE_PY = None

    def do_test(self, *args):
        popen_kwargs = dict(
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
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

    def run_python(self, *args):
        events = []

        popen_kwargs = dict(
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
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
