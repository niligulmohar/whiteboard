
from gi.repository import GLib

import dbus
from dbus.mainloop.glib import DBusGMainLoop

DBUS_NAME = 'org.freedesktop.Avahi'
DBUS_INTERFACE_SERVER = DBUS_NAME + '.Server'
DBUS_PATH_SERVER = '/'
DBUS_INTERFACE_SERVICE_BROWSER = DBUS_NAME + '.ServiceBrowser'

IF_UNSPEC = -1
PROTO_UNSPEC = -1


def new_service(interface, protocol, name, service_type, domain, flags):
    print('new_service',
          (interface, protocol, name, service_type, domain, flags))
    server.ResolveService(int(interface),
                          int(protocol),
                          name,
                          service_type,
                          domain,
                          PROTO_UNSPEC,
                          dbus.UInt32(0),
                          reply_handler=service_resolved,
                          error_handler=print_error)


def service_resolved(*args):
    print('service_resolved', args)


def print_error(*args):
    print('print_error', args)


if __name__ == '__main__':
    DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()
    server = dbus.Interface(bus.get_object(DBUS_NAME, DBUS_PATH_SERVER),
                            DBUS_INTERFACE_SERVER)
    raw_service_type_browser = server.ServiceBrowserNew(IF_UNSPEC,
                                                        PROTO_UNSPEC,
                                                        '_workstation._tcp',
                                                        'local',
                                                        dbus.UInt32(0))
    service_type_browser = dbus.Interface(
        bus.get_object(DBUS_NAME, raw_service_type_browser),
        DBUS_INTERFACE_SERVICE_BROWSER
    )

    service_type_browser.connect_to_signal('ItemNew', new_service)

    GLib.MainLoop().run()
