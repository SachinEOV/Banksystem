import sys
from twisted.internet import reactor
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol


class SaveToFile(Protocol):
    """
    A protocol to save the HTTP response body to a local file.
    """
    def __init__(self, filename):
        self.filename = filename
        self.file = None

    def connectionMade(self):
        # Open the file in binary mode to write the content
        self.file = open(self.filename, 'wb')

    def dataReceived(self, data):
        # Write received data chunks to the file
        self.file.write(data)

    def connectionLost(self, reason):
        if reason.check(Exception):
            print(f"Connection lost: {reason.getErrorMessage()}")
        else:
            print(f"Page successfully downloaded to {self.filename}")
        self.file.close()

        # Ensure reactor.stop() is only called once
        if reactor.running:
            reactor.stop()


def download_page(url, filename):
    """
    Fetch a web page using Twisted's Agent and save it to a file.
    """
    agent = Agent(reactor)
    d = agent.request(
        b"GET",
        url.encode("ascii"),
        Headers({b"user-agent": [b"Twisted Web Client"]}),
    )

    def cbResponse(response):
        print(f"HTTP Response Code: {response.code}")
        proto = SaveToFile(filename)
        response.deliverBody(proto)
        return proto.file.close()

    def cbError(failure):
        print(f"An error occurred: {failure.getErrorMessage()}")

    d.addCallback(cbResponse)
    d.addErrback(cbError)
    d.addBoth(lambda _: reactor.callLater(0, reactor.stop))  # Ensures reactor stops after all tasks

    reactor.run()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python dlpage.py <URL> <filename>")
        sys.exit(1)

    # The URL is the first argument and the filename is the second
    download_page(sys.argv[1], sys.argv[2])
