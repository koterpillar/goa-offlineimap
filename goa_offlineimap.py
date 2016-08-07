"""Get the credentials for offlineimap from GNOME Online Accounts."""

from __future__ import print_function
from __future__ import unicode_literals

import sys
from functools import wraps

import dbus

OBJECT_MANAGER = 'org.freedesktop.DBus.ObjectManager'
PROPERTIES = 'org.freedesktop.DBus.Properties'

GOA_PATH = '/org/gnome/OnlineAccounts'
GOA_NAME = 'org.gnome.OnlineAccounts'
GOA_MANAGER_PATH = '/org/gnome/OnlineAccounts/Manager'
GOA_ACCOUNT = 'org.gnome.OnlineAccounts.Account'
GOA_ACCOUNT_MAIL = 'org.gnome.OnlineAccounts.Mail'
GOA_ACCOUNT_OAUTH2 = 'org.gnome.OnlineAccounts.OAuth2Based'


def memoize(func):
    """Decorate the function to save the result of the first call."""

    @wraps(func)
    def wrapped():
        try:
            return func.result
        except AttributeError:
            pass

        func.result = func()
        return func.result

    return wrapped


@memoize
def session_bus():
    """The session bus."""
    return dbus.SessionBus()


@memoize
def get_account():
    """Get the path to the only online account set up."""

    bus = session_bus()

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


@memoize
def get_imap_host():
    """Get the IMAP host."""

    return get_account().Get(GOA_ACCOUNT_MAIL, 'ImapHost',
                             dbus_interface=PROPERTIES)


@memoize
def get_imap_user_name():
    """Get the IMAP user name."""

    return str(get_account().Get(GOA_ACCOUNT_MAIL, 'ImapUserName',
                                 dbus_interface=PROPERTIES))


@memoize
def get_client_id():
    """Get the client ID from the online account."""

    return str(get_account().Get(GOA_ACCOUNT_OAUTH2, 'ClientId',
                                 dbus_interface=PROPERTIES))


@memoize
def get_client_secret():
    """Get the client secret from the online account."""

    return str(get_account().Get(GOA_ACCOUNT_OAUTH2, 'ClientSecret',
                                 dbus_interface=PROPERTIES))


@memoize
def get_access_token():
    """Get the access token from the online account."""

    account = get_account()

    account.EnsureCredentials(dbus_interface=GOA_ACCOUNT)
    access_token, _ = account.GetAccessToken(dbus_interface=GOA_ACCOUNT_OAUTH2)
    return str(access_token)
