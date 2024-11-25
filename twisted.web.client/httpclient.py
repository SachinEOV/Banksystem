#!/usr/bin/env python
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
This example demonstrates how to make a simple HTTP client.

Usage:
    httpclient.py <url> [output_file]

Don't forget the http:// or https:// when you type the web address!
"""

import sys
from pprint import pprint
from twisted import version
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.python import log
from twisted.web.client import Agent, ResponseDone, BrowserLikePolicyForHTTPS
from twisted.web.http_headers import Headers


class SaveToFile(Protocol):
    """
    A protocol to save the HTTP response body to a file.
    """

    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, 'wb')
        self.onConnLost = Deferred()

    def connectionMade(self):
        print(f"Saving response to {self.filename}")

    def dataReceived(self, data):
        """
        Write received data to the file.
        """
        self.file.write(data)

    def connectionLost(self, reason):
        self.file.close()
        if not reason.check(ResponseDone):
            print(f"Download failed: {reason.getErrorMessage()}")
        else:
            print(f"Download complete. File saved to {self.filename}")
        self.onConnLost.callback(None)


class PrintToConsole(Protocol):
    """
    A protocol to print the HTTP response body to the console.
    """

    def connectionMade(self):
        self.buffer = b""
        self.onConnLost = Deferred()

    def dataReceived(self, data):
        """
        Buffer and print data as received.
        """
        self.buffer += data

    def connectionLost(self, reason):
        if not reason.check(ResponseDone):
            print(f"Connection lost: {reason.getErrorMessage()}")
        else:
            print("Response received:")
            print(self.buffer.decode("utf-8"))
        self.onConnLost.callback(None)


def main(reactor, url, output_file=None):
    """
    Create a custom UserAgent and send a GET request to a web server.
    """
    userAgent = f"Twisted/{version.short()} (httpclient.py)".encode("ascii")
    agent = Agent(reactor, BrowserLikePolicyForHTTPS())

    # Send the request
    d = agent.request(
        b"GET",
        url.encode("ascii"),
        Headers({b"user-agent": [userAgent]}),
    )

    def cbResponse(response):
        """
        Handle the HTTP response.
        """
        pprint(vars(response))
        if response.length is not None:
            print(f"Response body will consist of {response.length} bytes.")
        else:
            print("Response body length is unknown.")

        if output_file:
            proto = SaveToFile(output_file)
        else:
            proto = PrintToConsole()
        
        response.deliverBody(proto)
        return proto.onConnLost

    def handleError(failure):
        print(f"Error: {failure.getErrorMessage()}")

    d.addCallback(cbResponse)
    d.addErrback(handleError)
    d.addBoth(lambda ign: reactor.stop())

    reactor.run()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: httpclient.py <url> [output_file]")
        sys.exit(1)
    main(reactor, sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
