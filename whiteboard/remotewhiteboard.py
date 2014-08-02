
class RemoteWhiteboard(object):
    def __init__(self, name, address):
        self.name = name
        self.address = address

    def __repr__(self):
        return '<RemoteWhiteboard {}@{}>'.format(self.name, self.address)
