
from gi.repository import Gio
import nacl.public


class LocalWhiteboard(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.private_key = nacl.public.PrivateKey.generate()
        self.public_key = self.private_key.public_key
        self.socket_service = None

    def publish(self):
        self.parent.add_service_for_whiteboard(self)
        if self.socket_service is None:
            self.socket_service = Gio.SocketService()
            self.socket_service.add_inet_port(self.parent.port)
            self.socket_service.connect('incoming', self.on_incoming)
        self.socket_service.start()

    def on_incoming(self, *args):
        print('on_incoming', args)

    def unpublish(self):
        self.parent.remove_service_for_whiteboard(self)
        self.socket_service.stop()
