from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory
from twisted.internet.endpoints import TCP4ServerEndpoint

class Server(Protocol):
    def connectionMade(self):
        print("New connection established.")
        self.transport.write("Hello from server.\n".encode("utf-8"))

    def dataReceived(self, data):
        message = data.decode("utf-8").strip()
        print(f"Received from client: {message}")
        
        if message.lower() == "hi":
            response = "Hey there!"
        elif message.lower() == "how are you":
            response = "I'm good, thank you!"
        else:
            response = f"Received your message: {message}"
        
        self.transport.write(f"{response}\n".encode("utf-8"))

class ServerFactory(Factory):
    def buildProtocol(self, addr):
        return Server()

if __name__ == "__main__":
    endpoint = TCP4ServerEndpoint(reactor, 9000)
    endpoint.listen(ServerFactory())
    print("Server is running on port 9000...")
    reactor.run()
