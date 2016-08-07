#!/usr/bin/env python3
"""Get the credentials for offlineimap from Gnome Online Accounts."""

import sys

import dbus

OBJECT_MANAGER = 'org.freedesktop.DBus.ObjectManager'
PROPERTIES = 'org.freedesktop.DBus.Properties'

GOA_PATH = '/org/gnome/OnlineAccounts'
GOA_NAME = 'org.gnome.OnlineAccounts'
GOA_MANAGER_PATH = '/org/gnome/OnlineAccounts/Manager'
GOA_ACCOUNT = 'org.gnome.OnlineAccounts.Account'
GOA_ACCOUNT_OAUTH2 = 'org.gnome.OnlineAccounts.OAuth2Based'


def get_account(bus):
    """Get the path to the only online account set up."""

    goa_manager = bus.get_object(GOA_NAME, GOA_PATH)

    goa_objects = goa_manager.GetManagedObjects(dbus_interface=OBJECT_MANAGER)

    accounts = [
        obj for obj in goa_objects
        if obj != GOA_MANAGER_PATH
    ]

    if len(accounts) > 1:
        sys.exit("More than one account found.")

    (account_path,) = accounts

    return bus.get_object(GOA_NAME, account_path)


def get_client_id(account):
    """Get the client ID from the online account."""

    return account.Get(GOA_ACCOUNT_OAUTH2, 'ClientId',
                       dbus_interface=PROPERTIES)


def get_client_secret(account):
    """Get the client secret from the online account."""

    return account.Get(GOA_ACCOUNT_OAUTH2, 'ClientSecret',
                       dbus_interface=PROPERTIES)


def get_access_token(account):
    """Get the access token from the online account."""

    account.EnsureCredentials(dbus_interface=GOA_ACCOUNT)
    access_token, _ = account.GetAccessToken(dbus_interface=GOA_ACCOUNT_OAUTH2)
    return access_token


def main():
    """Print the account credentials."""

    bus = dbus.SessionBus()

    account = get_account(bus)

    print(
        get_client_id(account),
        get_client_secret(account),
        get_access_token(account),
    )

if __name__ == '__main__':
    main()
