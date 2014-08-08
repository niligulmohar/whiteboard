
from gi.repository import Gio


class RemoteWhiteboard(object):
    def __init__(self, name, address, port):
        self.name = name
        self.address = address
        self.port = port
        self.socket_address = Gio.InetSocketAddress.new_from_string(address,
                                                                    port)

    def connect(self):
        client = Gio.SocketClient()
        connection = client.connect(self.socket_address)
        connection.close()

    def __repr__(self):
        return '<RemoteWhiteboard {}@{}:{}>'.format(self.name,
                                                    self.address,
                                                    self.port)
