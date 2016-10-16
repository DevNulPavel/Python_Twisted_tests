#! /bin/env python3

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
# from twisted.internet import epollreactor
from twisted.internet import reactor
import sys,time


class glob():
    connections=0
    crefuse=0
    clost=0
    def enchant(self):
        self.connections+=1
    def refuse(self):
        self.crefuse+=1
    def lost(self):
        self.clost+=1


class EchoClient(LineReceiver):
    measure=True

    def connectionMade(self):
        #print("New connection")
        self.sendLine("Hello, world!".encode())
        self.t1 = time.time()

    def lineReceived(self, line):
        if self.measure:
            self.t2 = time.time() - self.t1
            file.write('%s    %s    %s    %s    %s\n' % (a.connections+1, self.t2,a.crefuse,a.clost,line))
            self.measure=False
            if a.connections+1 < clients:
                a.enchant()
                reactor.connectTCP(host, port, EchoClientFactory())
            else:
                self.transport.loseConnection()


class EchoClientFactory(ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        a.refuse()

    def clientConnectionLost(self, connector, reason):
        a.lost()



# epollreactor.install()

clients=30000
host='127.0.0.1'
port=1234
file = open( 'log.dat', 'w')
a=glob()


def main():
    f = EchoClientFactory()

    reactor.connectTCP(host, port, f)
    reactor.run()
    file.close()

if __name__ == '__main__':
    main()



