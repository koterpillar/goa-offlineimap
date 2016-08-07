GNOME Online Accounts for offlineimap
=====================================

Use credentials from GNOME Online Accounts in offlineimap.

Work in progress, intended to work with a single GMail account only.

To use:

    [general]
    pythonfile = /path/to/goa_offlineimap.py

    [Repository Remote]
    type = Gmail
    auth_mechanisms = XOAUTH2
    remoteusereval = get_imap_user_name()
    oauth2_client_id_eval = lambda _: get_client_id()
    oauth2_client_secret_eval = lambda _: get_client_secret()
    oauth2_access_token_eval = lambda _: get_access_token()

    # The following are implemented but not needed for Gmail
    # remotehosteval = get_imap_host()
