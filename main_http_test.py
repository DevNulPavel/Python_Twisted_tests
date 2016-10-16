#! /bin/env python3

from twisted.web import server, resource
from twisted.internet import reactor, endpoints

class Counter(resource.Resource):
    isLeaf = True
    numberRequests = 0

    def render_GET(self, request):
        # self.numberRequests += 1
        # request.setHeader(b"content-type", b"text/plain")
        content = ""
        return content.encode("ascii")

endpoints.serverFromString(reactor, "tcp:8800").listen(server.Site(Counter()))
reactor.run()