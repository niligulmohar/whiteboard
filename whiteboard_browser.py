from gi.repository import GLib

import whiteboard


def on_update(whiteboards):
    print(whiteboards)


if __name__ == '__main__':
    whiteboards = whiteboard.Whiteboards('potatis', 4711)
    whiteboards.subscribe(on_update)

    GLib.MainLoop().run()
