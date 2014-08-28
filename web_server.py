from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from application import app

http_server = HTTPServer(WSGIContainer(app))
http_server.listen(19000) #expected port - should be configurable
IOLoop.instance().start()