
# List workstations through the Avahi GObject bindings

from gi.repository import Avahi, GLib


def connect_debug_callback(subject, signal):
    def callback(*args):
        print((subject, signal), args)

    subject.connect(signal, callback)


def on_new_service(browser, interface, protocol, name, type, domain, flags):
    print((browser, 'new-service'),
          (browser, interface, protocol, name, type, domain, flags))
    resolver = Avahi.ServiceResolver(
        interface=interface,
        protocol=protocol,
        name=name,
        type=type,
        domain=domain,
        aprotocol=Avahi.Protocol.GA_PROTOCOL_UNSPEC
    )
    connect_debug_callback(resolver, 'failure')
    resolver.connect('found', on_resolved_service)
    resolver.attach(client)


def on_resolved_service(resolver,
                        interface,
                        protocol,
                        name,
                        avahi_type,
                        domain,
                        fqdn,
                        macaddress,
                        port,
                        _,
                        flags):
    print('{} is {}'.format(name, fqdn))


if __name__ == '__main__':
    client = Avahi.Client()
    connect_debug_callback(client, 'state-changed')
    client.start()

    service_browser = Avahi.ServiceBrowser(
        type='_workstation._tcp',
        protocol=Avahi.Protocol.GA_PROTOCOL_UNSPEC,
        interface=-1
    )
    for signal in ('removed-service',
                   'all-for-now',
                   'cache-exhausted',
                   'failure'):
        connect_debug_callback(service_browser, signal)
    service_browser.connect('new-service', on_new_service)
    service_browser.attach(client)

    GLib.MainLoop().run()
