import dbus
bus = dbus.SessionBus()

proxy = bus.get_object('org.gnome.SettingsDaemon',
                       '/org/gnome/SettingsDaemon/Power')

iface=dbus.Interface(proxy,dbus_interface='org.gnome.SettingsDaemon.Power.Screen')

iface.SetPercentage(30)
