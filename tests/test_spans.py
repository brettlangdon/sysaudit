import os

from .base import BaseTest


class SubscribeTest(BaseTest):
    TEST_FILE_PY = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "span-tests.py")
    )

    def test_properties(self):
        self.do_test("test_properties")

    def test_started_ended(self):
        self.do_test("test_started_ended")

    def test_started_ended_contextmanager(self):
        self.do_test("test_started_ended_contextmanager")

    def test_lifecycle_events(self):
        self.do_test("test_lifecycle_events")

    def test_lifecycle_events_contextmanager(self):
        self.do_test("test_lifecycle_events_contextmanager")

    def test_lifecycle_events_data(self):
        self.do_test("test_lifecycle_events_data")

    def test_end_before_start(self):
        self.do_test("test_end_before_start")

    def test_custom_message(self):
        self.do_test("test_custom_message")

    def test_annotate_message(self):
        self.do_test("test_custom_message")
