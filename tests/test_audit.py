"""Tests for sys.audit and sys.addaudithook

https://github.com/python/cpython/blob/b676f5f809007533db3e3fdd01243959dd233d57/Lib/test/test_audit.py
"""
import importlib
import os
import subprocess
import sys
import unittest


AUDIT_TESTS_PY = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "audit-tests.py")
)

skip_old_py = unittest.skipIf(
    sys.version_info < (3, 8), "Skipping tests testing built-in events"
)


class AuditTest(unittest.TestCase):
    def do_test(self, *args):
        popen_kwargs = dict(
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if sys.version_info >= (3, 6):
            popen_kwargs["encoding"] = "utf-8"

        p = subprocess.Popen(
            [sys.executable, AUDIT_TESTS_PY] + list(args), **popen_kwargs
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
            [sys.executable, AUDIT_TESTS_PY] + list(args), **popen_kwargs
        )
        p.wait()
        sys.stderr.writelines(p.stderr)
        return (
            p.returncode,
            [line.strip().partition(" ") for line in p.stdout],
            "".join(p.stderr),
        )

    def test_basic(self):
        self.do_test("test_basic")

    def test_block_add_hook(self):
        self.do_test("test_block_add_hook")

    def test_block_add_hook_baseexception(self):
        self.do_test("test_block_add_hook_baseexception")

    @skip_old_py
    def test_pickle(self):
        importlib.import_module("pickle")

        self.do_test("test_pickle")

    @skip_old_py
    def test_monkeypatch(self):
        self.do_test("test_monkeypatch")

    @skip_old_py
    def test_open(self):
        TESTFN = "@test_{}_tmp".format(os.getpid())
        self.do_test("test_open", TESTFN)

    @skip_old_py
    def test_cantrace(self):
        self.do_test("test_cantrace")

    @skip_old_py
    def test_mmap(self):
        self.do_test("test_mmap")

    @skip_old_py
    def test_excepthook(self):
        returncode, events, stderr = self.run_python("test_excepthook")
        if not returncode:
            self.fail("Expected fatal exception\n{}".format(stderr))

        self.assertSequenceEqual(
            [("sys.excepthook", " ", "RuntimeError('fatal-error')")], events
        )

    @skip_old_py
    def test_unraisablehook(self):
        returncode, events, stderr = self.run_python("test_unraisablehook")
        if returncode:
            self.fail(stderr)

        self.assertEqual(events[0][0], "sys.unraisablehook")
        self.assertEqual(
            events[0][2],
            "RuntimeError('nonfatal-error') Exception ignored for audit hook test",
        )

    @skip_old_py
    def test_winreg(self):
        try:
            importlib.import_module("winreg")
        except ImportError as msg:
            raise unittest.SkipTest(str(msg))

        returncode, events, stderr = self.run_python("test_winreg")
        if returncode:
            self.fail(stderr)

        self.assertEqual(events[0][0], "winreg.OpenKey")
        self.assertEqual(events[1][0], "winreg.OpenKey/result")
        expected = events[1][2]
        self.assertTrue(expected)
        self.assertSequenceEqual(
            ["winreg.EnumKey", " ", "{} 0".format(expected)], events[2]
        )
        self.assertSequenceEqual(
            ["winreg.EnumKey", " ", "{} 10000".format(expected)], events[3]
        )
        self.assertSequenceEqual(["winreg.PyHKEY.Detach", " ", expected], events[4])

    @skip_old_py
    def test_socket(self):
        importlib.import_module("socket")
        returncode, events, stderr = self.run_python("test_socket")
        if returncode:
            self.fail(stderr)

        self.assertEqual(events[0][0], "socket.gethostname")
        self.assertEqual(events[1][0], "socket.__new__")
        self.assertEqual(events[2][0], "socket.bind")
        self.assertTrue(events[2][2].endswith("('127.0.0.1', 8080)"))


if __name__ == "__main__":
    unittest.main()
