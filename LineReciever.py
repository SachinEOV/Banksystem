from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver

class ChatProtocol(LineReceiver):
    def connectionMade(self):
        self.sendLine(b"Welcome to the chat server!")
        self.sendLine(b"Type 'hi', 'how are you', 'what is twisted','where is EOV located', or 'bye'.")

    def lineReceived(self, line):
        message = line.decode('utf-8').strip().lower()
        print(f"Received message: {message}")

        responses = {
            "hi": "Hey there!",
            "how are you": "I am good!",
            "what is twisted": "Twisted is an event-driven networking engine in Python.",
            "where is EOV located": "EOV is located in Pune",
            "bye": "Goodbye! Have a nice day!"
        }

        response = responses.get(message, "I didn't understand that. Try asking something else!")
        self.sendLine(response.encode('utf-8'))

        if message == "bye":
            self.transport.loseConnection()

class ChatFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return ChatProtocol()

reactor.listenTCP(9000, ChatFactory())
print("Chat Server is running on port 9000...")
reactor.run()
