import os

from .base import BaseTest


class SubscribeTest(BaseTest):
    TEST_FILE_PY = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "subscribe-tests.py")
    )

    def test_basic(self):
        self.do_test("test_basic")

    def test_multiple_hooks(self):
        self.do_test("test_multiple_hooks")
