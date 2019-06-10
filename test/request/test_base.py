from tortoise import Tortoise
from tortoise.models import Model
from unittest.mock import MagicMock
from collections import namedtuple
from libkol import models
import unittest
import asyncio
from os import path

TEST_DATA = path.join(path.dirname(path.abspath(__file__)), "test_data")


def open_test_data(request, variant: str, ext: str = "html"):
    return open(path.join(TEST_DATA, "{}_{}.{}".format(request, variant, ext)))


class MockSession:
    def __init__(self, test, request_mocks):
        Response = namedtuple(
            "ClientResponse", ["url", "content", "get_encoding", "text"]
        )

        def async_return(url, *args, **kwargs):
            data_file = request_mocks.get(url, None)

            if data_file is None:
                content = ""
            else:
                try:
                    file = open_test_data(test.request, data_file)
                    content = file.read()
                    file.close()
                except:
                    content = data_file

            request = asyncio.Future()
            text = asyncio.Future()
            text.set_result(content)
            response = Response(
                url=url,
                content=content,
                get_encoding=lambda: "utf-8",
                text=lambda *args: text,
            )
            request.set_result(response)
            request.url = url
            return request

        self.request = MagicMock(side_effect=async_return)


class TestCase(unittest.TestCase):
    request: str
    db_file = path.join(path.dirname(__file__), "../../libkol/libkol.db")

    def run_async(self, data, async_test, ext: str = "html", request_mocks={}):
        event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(event_loop)

        session = MockSession(self, request_mocks)

        async def run_test():
            await Tortoise.init(
                db_url="sqlite://{}".format(self.db_file), modules={"models": models}
            )

            Model.kol = session

            try:
                with open_test_data(self.request, data, ext) as file:
                    await async_test(file)
            finally:
                await Tortoise.close_connections()
                event_loop.stop()

        coro = asyncio.coroutine(run_test)
        event_loop.run_until_complete(coro())
        event_loop.close()

        return session
