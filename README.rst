=============================
python-apns
=============================

A library for interacting with APNs using HTTP/2 and token based authentication. 




Installation 
-----------------

::

    pip install gobiko.apns


Usage
-----------------

Create a client::

    from gobiko.apns import APNsClient
    
    client = APNsClient(
        team_id=TEAM_ID, 
        bundle_id=BUNDLE_ID, 
        auth_key_id=APNS_KEY_ID, 
        auth_key_filepath=APNS_KEY_FILEPATH, 
        use_sandbox=True
    )


Alternatively, you can create a client with the contents of the auth key file directly::

    client = APNsClient(
        team_id=TEAM_ID, 
        bundle_id=BUNDLE_ID, 
        auth_key_id=APNS_KEY_ID, 
        auth_key=APNS_KEY, 
        use_sandbox=True
    )

Now you can send a message to a device by specifying its registration ID::

    client.send_message(
        registration_id, 
        "All your base are belong to us."
    )

Or you can send bulk messages to a list of devices::

    client.send_bulk_message(
        [registration_id_1, registration_id_2], 
        "You have no chance to survive, make your time."
    )


Documentation
-----------------

- More information on APNs and an explanation of the above can be found `in this blog post <http://gobiko.com/blog/token-based-authentication-http2-example-apns/>`_.

- Apple documentation for APNs can be found `here <https://developer.apple.com/library/content/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/APNSOverview.html#//apple_ref/doc/uid/TP40008194-CH8-SW1>`_.
