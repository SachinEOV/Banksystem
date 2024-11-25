from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet.endpoints import TCP4ClientEndpoint

class Client(Protocol):
    def connectionMade(self):
        print("Connected to the server.")
        self.send_data()

    def dataReceived(self, data):
        print("Server:", data.decode("utf-8").strip())
        self.send_data()

    def send_data(self):
        user_input = input("You: ")
        self.transport.write(user_input.encode("utf-8"))

class ClientFactory(ClientFactory):
    def buildProtocol(self, addr):
        return Client()

if __name__ == "__main__":
    endpoint = TCP4ClientEndpoint(reactor, "localhost", 9000)
    endpoint.connect(ClientFactory())
    print("Client is connecting to the server on port 9000...")
    reactor.run()
