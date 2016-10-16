from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

# обхект, который обрабатывает отдельное соединение
class Chat(LineReceiver):
    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GETNAME"

    def connectionMade(self):
        self.sendLine("Имя в чате:".encode())

    def connectionLost(self, reason):
        if self.name in self.users:
            del self.users[self.name]

    def lineReceived(self, line):
        if self.state == "GETNAME":
            self.handle_GETNAME(line)
        else:
            self.handle_CHAT(line)

    def handle_GETNAME(self, name):
        if name in self.users:
            self.sendLine("Имя занято.".encode())
            return

        text = "Халлоу, %s!" % (str(name))
        self.sendLine(text.encode())
        self.name = name
        self.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        if message == b"exit":
            self.transport.loseConnection()
            return

        message = "<%s> %s" % (self.name, str(message))
        for name in self.users.keys():
            protocol = self.users[name]
            if protocol != self:
                protocol.sendLine(message.encode())


# Объект с общими данными, создает обработчики
class ChatFactory(Factory):
    def __init__(self):
        self.users = {}     # maps user names to Chat instances

    def buildProtocol(self, addr):
        return Chat(self.users)


if __name__ == '__main__':
    reactor.listenTCP(1234, ChatFactory())
    reactor.run()