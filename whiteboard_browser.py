from gi.repository import GLib

import whiteboard


def on_update(whiteboards):
    if len(whiteboards) > 0:
        list(whiteboards.values())[0].connect()


if __name__ == '__main__':
    whiteboards = whiteboard.Whiteboards('potatis', 4711)
    whiteboards.subscribe(on_update)

    GLib.MainLoop().run()
