import json

from libkol.request import chat_send

from .test_base import TestCase


class ChatSendTestCase(TestCase):
    request = "chat_send"

    def test_chat_send_no_respose(self):
        async def run_test(file):
            result = await chat_send.parser(json.load(file))
            self.assertEqual(result.msgs, [])
            self.assertEqual(result.output, "")

        self.run_async("no_response", run_test, "json")

    def test_chat_send_green_response(self):
        async def run_test(file):
            result = await chat_send.parser(json.load(file))
            self.assertEqual(result.msgs, [])
            self.assertNotEqual(result.output, "")

        self.run_async("green_response", run_test, "json")
