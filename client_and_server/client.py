from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint

class Client(Protocol):
    def connectionMade(self):
        print("Connected to the server")
        self.transport.write(input("::: ").encode("utf-8"))

    def dataReceived(self, data):
        print("Received from server:", data.decode("utf-8"))
        self.transport.write(input("::: ").encode("utf-8"))

class MyClientFactory(ClientFactory):
    def buildProtocol(self, addr):
        return Client()

if __name__ == "__main__":
    endpoint = TCP4ClientEndpoint(reactor, 'localhost', 9000)
    endpoint.connect(MyClientFactory())
    print("Connecting to server on port 8007...")
    reactor.run()
