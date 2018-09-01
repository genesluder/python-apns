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

If you run into any problems deserializing the key, try wrapping it to 64 lines::

    client = APNsClient(
        team_id=TEAM_ID,
        bundle_id=BUNDLE_ID,
        auth_key_id=APNS_KEY_ID,
        auth_key=APNS_KEY,
        use_sandbox=True,
        wrap_key=True
    )

In Python 2.x environments, you may need to force the communication protocol to 'h2'::

    client = APNsClient(
        team_id=TEAM_ID,
        bundle_id=BUNDLE_ID,
        auth_key_id=APNS_KEY_ID,
        auth_key=APNS_KEY,
        use_sandbox=True,
        force_proto='h2'
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


Payload
-----------------

Additional APNs payload values can be passed as kwargs::

    client.send_message(
        registration_id, 
        "All your base are belong to us.", 
        badge=None, 
        sound=None, 
        category=None, 
        content_available=False,
        action_loc_key=None, 
        loc_key=None, 
        loc_args=[], 
        extra={}, 
        identifier=None, 
        expiration=None, 
        priority=10, 
        topic=None
    )


Pruning
-----------------

The legacy binary interface APNs provided an endpoint to check whether a registration ID had 
become inactive. Now the service returns a BadDeviceToken error when you attempt to deliver an 
alert to an inactive registration ID. If you need to prune inactive IDs from a database you 
can handle the BadDeviceToken exception to do so::

    from gobiko.apns.exceptions import BadDeviceToken

    try:
        client.send_message(OLD_REGISTRATION_ID, "Message to an invalid registration ID.")
    except BadDeviceToken:
        # Handle invalid ID here
        pass

Same approach if sending by bulk::

    from gobiko.apns.exceptions import PartialBulkMessage
    
    try:
        client.send_bulk_message([registration_id1, registration_id2], "Message")
    except PartialBulkMessage as e:
        # Handle list of invalid IDs using e.bad_registration_ids
        pass


Documentation
-----------------

- More information on APNs and an explanation of the above can be found `in this blog post <http://gobiko.com/blog/token-based-authentication-http2-example-apns/>`_.

- Apple documentation for APNs can be found `here <https://developer.apple.com/library/content/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/APNSOverview.html#//apple_ref/doc/uid/TP40008194-CH8-SW1>`_.


Credits
-----------------


