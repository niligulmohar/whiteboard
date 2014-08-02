
from gi.repository import GLib

import dbus
from dbus.mainloop.glib import DBusGMainLoop

DBUS_NAME = 'org.freedesktop.Avahi'
DBUS_INTERFACE_SERVER = DBUS_NAME + '.Server'
DBUS_PATH_SERVER = '/'
DBUS_INTERFACE_ENTRY_GROUP = DBUS_NAME + ".EntryGroup"

IF_UNSPEC = -1
PROTO_UNSPEC = -1


def print_args(*args):
    print('print_args', args)


def dump(obj):
    print(type(obj), obj)


def state_changed(*args):
    print('state_changed', args)


if __name__ == '__main__':
    DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()
    server_proxy = bus.get_object(DBUS_NAME, DBUS_PATH_SERVER)
    server = dbus.Interface(server_proxy, DBUS_INTERFACE_SERVER)
    # server.connect_to_signal('StateChanged', state_changed)
    # server_proxy.Ping(dbus_interface='org.freedesktop.DBus.Peer')
    entry_group_path = server.EntryGroupNew()
    entry_group_proxy = bus.get_object(DBUS_NAME, entry_group_path)
    entry_group = dbus.Interface(entry_group_proxy, DBUS_INTERFACE_ENTRY_GROUP)
    if entry_group.IsEmpty():
        entry_group.AddService(
            IF_UNSPEC,
            PROTO_UNSPEC,
            0,
            'Potatis',
            '_potatis._tcp',
            '',
            '',
            4711,
            [b'Gillar potatis=Tomtar']
        )
        entry_group.Commit()

    GLib.MainLoop().run()
