# Copyright (c) Twisted Matrix Laboratories
# See LICENSE for details.

"""
This program will retrieve and print the resource at the given URL.

Usage:
    $ python getpage.py <URL>
"""

import sys
from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol


class PrintResponse(Protocol):
    """
    A protocol to print the HTTP response body to the console.
    """

    def connectionMade(self):
        self.buffer = b""
        self.onConnLost = Deferred()

    def dataReceived(self, data):
        self.buffer += data

    def connectionLost(self, reason):
        if reason.check(Exception):
            print(f"Connection lost: {reason.getErrorMessage()}")
        else:
            print("Response received:")
            print(self.buffer.decode("utf-8"))
        self.onConnLost.callback(None)


def fetch_page(url):
    """
    Fetch a web page using Twisted's Agent.
    """
    agent = Agent(reactor)
    d = agent.request(
        b"GET",
        url.encode("ascii"),
        Headers({b"user-agent": [b"Twisted Web Client"]}),
    )

    def cbResponse(response):
        print(f"HTTP Response Code: {response.code}")
        proto = PrintResponse()
        response.deliverBody(proto)
        return proto.onConnLost

    def cbError(failure):
        print(f"An error occurred: {failure.getErrorMessage()}")

    d.addCallback(cbResponse)
    d.addErrback(cbError)
    d.addBoth(lambda _: reactor.stop())

    reactor.run()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python getpage.py https://www.google.com")
        sys.exit(1)

    fetch_page(sys.argv[1])
