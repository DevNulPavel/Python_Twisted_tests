#! /bin/env python3

# Read username, output from non-empty factory, drop connections
# Use deferreds, to minimize synchronicity assumptions

from twisted.internet import protocol, reactor, defer, endpoints
from twisted.protocols import basic

class FingerProtocol(basic.LineReceiver):
    def lineReceived(self, user):
        d = self.factory.getUser(user)

        def onError(err):
            return 'Internal error in server'

        def writeResponse(message):
            result = message + '\r\n'
            self.transport.write(result.encode())
            self.transport.loseConnection()

        d.addErrback(onError)
        d.addCallback(writeResponse)


class FingerFactory(protocol.ServerFactory):
    protocol = FingerProtocol

    def __init__(self, data):
        self.users = data

    def getUser(self, user):
        deferred = defer.Deferred()

        userStr = user.decode()
        result = self.users.get(userStr, "No such user")

        # Эмуляция долгого запроса
        reactor.callLater(2, deferred.callback, result)

        return deferred


dictData = {"test": "contains"}

fingerEndpoint = endpoints.serverFromString(reactor, "tcp:1234")
fingerEndpoint.listen(FingerFactory(dictData))

reactor.run()