import dbus
from dbus.mainloop.glib import DBusGMainLoop

from .whiteboard import Whiteboard
from .remotewhiteboard import RemoteWhiteboard

AVAHI_DBUS_NAME = 'org.freedesktop.Avahi'
AVAHI_INTERFACE_UNSPEC = -1
AVAHI_PROTOCOL_UNSPEC = -1


class Whiteboards(object):
    def __init__(self, whiteboard_type, port):
        self.whiteboard_type = '_{}_whiteboard._tcp'.format(whiteboard_type)
        self.port = port

        self.avahi_server = None
        self.bus = None

        self.service_browser = None
        self.entry_group = None

        self.published_whiteboards = []
        self.discovered_whiteboards = {}
        self.subscription_callbacks = []

    def ensure_dbus_initialized(self):
        if self.avahi_server is None:
            DBusGMainLoop(set_as_default=True)
            self.bus = dbus.SystemBus()
            avahi_server_proxy = self.bus.get_object(AVAHI_DBUS_NAME, '/')
            self.avahi_server = dbus.Interface(avahi_server_proxy,
                                               AVAHI_DBUS_NAME + '.Server')

    def on_found_service(self,
                         interface,
                         protocol,
                         name,
                         service_type,
                         domain,
                         flags):
        self.avahi_server.ResolveService(
            interface,
            protocol,
            name,
            service_type,
            domain,
            AVAHI_PROTOCOL_UNSPEC,
            dbus.UInt32(0),
            reply_handler=self.on_service_resolved,
            error_handler=self.on_error
        )

    def on_service_resolved(self,
                            interface,
                            protocol,
                            name,
                            service_type,
                            domain,
                            fqdn,
                            address_protocol,
                            address,
                            port,
                            txt,
                            flags):
        discovery = RemoteWhiteboard(name, address)
        self.discovered_whiteboards[str(name)] = discovery
        self.notify_subscribers()

    def on_error(self, *args):
        print('on_error', args)

    def on_lost_service(self,
                        interface,
                        protocol,
                        name,
                        service_type,
                        domain,
                        flags):
        del self.discovered_whiteboards[str(name)]
        self.notify_subscribers()

    def ensure_service_browser_initialized(self):
        self.ensure_dbus_initialized()
        if self.service_browser is None:
            service_browser_path = self.avahi_server.ServiceBrowserNew(
                AVAHI_INTERFACE_UNSPEC,
                AVAHI_PROTOCOL_UNSPEC,
                self.whiteboard_type,
                # '_workstation._tcp',
                'local',
                0
            )
            service_browser_proxy = self.bus.get_object(AVAHI_DBUS_NAME,
                                                        service_browser_path)
            self.service_browser = dbus.Interface(
                service_browser_proxy,
                AVAHI_DBUS_NAME + '.ServiceBrowser'
            )
            self.service_browser.connect_to_signal('ItemNew',
                                                   self.on_found_service)
            self.service_browser.connect_to_signal('ItemRemove',
                                                   self.on_lost_service)

    def list(self):
        self.ensure_service_browser_initialized()
        return self.discovered_whiteboards

    def subscribe(self, callback):
        self.ensure_service_browser_initialized()
        if callback not in self.subscription_callbacks:
            self.subscription_callbacks.append(callback)
            callback(self.discovered_whiteboards)

    def unsubscribe(self, callback):
        self.ensure_service_browser_initialized()
        if callback in self.subscription_callbacks:
            self.subscription_callbacks.remove(callback)

    def notify_subscribers(self):
        for callback in self.subscription_callbacks:
            callback(self.discovered_whiteboards)

    def add_service_for_whiteboard(self, whiteboard):
        if whiteboard not in self.published_whiteboards:
            self.ensure_entry_group_initialized()
            self.add_service_to_entry_group(whiteboard)
            self.commit_services()
            self.published_whiteboards.append(whiteboard)

    def remove_service_for_whiteboard(self, whiteboard):
        self.published_whiteboards.remove(whiteboard)
        self.reset_services()
        self.ensure_entry_group_initialized()

    def ensure_entry_group_initialized(self):
        self.ensure_dbus_initialized()
        if self.entry_group is None:
            entry_group_path = self.avahi_server.EntryGroupNew()
            entry_group_proxy = self.bus.get_object(AVAHI_DBUS_NAME,
                                                    entry_group_path)
            self.entry_group = dbus.Interface(entry_group_proxy,
                                              AVAHI_DBUS_NAME + '.EntryGroup')
        if self.entry_group.IsEmpty() and len(self.published_whiteboards) > 0:
            for whiteboard in self.published_whiteboards:
                self.add_service_to_entry_group(whiteboard)
            self.commit_services()

    def add_service_to_entry_group(self, whiteboard):
            self.entry_group.AddService(
                AVAHI_INTERFACE_UNSPEC,
                AVAHI_PROTOCOL_UNSPEC,
                0,
                whiteboard.name,
                self.whiteboard_type,
                '',
                '',
                4711,
                []
            )

    def reset_services(self):
        self.entry_group.Reset()

    def commit_services(self):
        self.entry_group.Commit()

    def new_whiteboard(self, name):
        return Whiteboard(self, name)
