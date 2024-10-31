from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ServerFactory
from twisted.internet.endpoints import TCP4ServerEndpoint

class Server(Protocol):
    def connectionMade(self):
        print("New Connection")
        self.transport.write("Hello from the server".encode("utf-8"))

    def dataReceived(self, data):
        print("Received from client:", data.decode("utf-8"))
        self.transport.write(data)

class MyServerFactory(ServerFactory):
    def buildProtocol(self, addr):
        return Server()

if __name__ == "__main__":
    endpoint = TCP4ServerEndpoint(reactor, 9001)  
    endpoint.listen(MyServerFactory())
    print("Server is running on port 9001...") 
    reactor.run()
