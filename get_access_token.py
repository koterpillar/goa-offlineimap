#!/usr/bin/env python3
"""Get the credentials for offlineimap from Gnome Online Accounts."""

import sys

import dbus


GOA_PATH = '/org/gnome/OnlineAccounts'
GOA_NAME = 'org.gnome.OnlineAccounts'
GOA_MANAGER_PATH = '/org/gnome/OnlineAccounts/Manager'
GOA_ACCOUNT = 'org.gnome.OnlineAccounts.Account'
GOA_ACCOUNT_OAUTH2 = 'org.gnome.OnlineAccounts.OAuth2Based'

bus = dbus.SessionBus()

goa_manager = bus.get_object(GOA_NAME, GOA_PATH)

goa_objects = goa_manager.GetManagedObjects(dbus_interface='org.freedesktop.DBus.ObjectManager')

accounts = [
    obj for obj in goa_objects
    if obj != GOA_MANAGER_PATH
]

if len(accounts) > 1:
    sys.exit("More than one account found.")

(account_path,) = accounts

account = bus.get_object(GOA_NAME, account_path)

account.EnsureCredentials(dbus_interface=GOA_ACCOUNT)
access_token, _ = account.GetAccessToken(dbus_interface=GOA_ACCOUNT_OAUTH2)
print(access_token)
