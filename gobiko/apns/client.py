import importlib
import json
import jwt
import time
import uuid

from collections import namedtuple
from contextlib import closing
from hyper import HTTP20Connection

from .exceptions import (
    InternalException,
    ImproperlyConfigured,
    PayloadTooLarge,
    BadDeviceToken,
    PartialBulkMessage,
    BadTopic,
    InvalidPushType,
)

from .utils import validate_private_key, wrap_private_key


ALGORITHM = 'ES256'
SANDBOX_HOST = 'api.development.push.apple.com:443'
PRODUCTION_HOST = 'api.push.apple.com:443'
MAX_NOTIFICATION_SIZE = 4096

APNS_PUSH_TYPES = ('alert', 'background', 'voip', 'complication', 'fileprovider', 'mdm')

APNS_RESPONSE_CODES = {
    'Success': 200,
    'BadRequest': 400,
    'TokenError': 403, 
    'MethodNotAllowed': 405,
    'TokenInactive': 410,
    'PayloadTooLarge': 413,
    'TooManyRequests': 429,
    'InternalServerError': 500, 
    'ServerUnavailable': 503,
}
APNSResponseStruct = namedtuple('APNSResponseStruct', APNS_RESPONSE_CODES.keys())
APNSResponse = APNSResponseStruct(**APNS_RESPONSE_CODES)


class APNsClient(object):

    def __init__(self, team_id, auth_key_id, 
            auth_key=None, auth_key_filepath=None, bundle_id=None, use_sandbox=False, force_proto=None, wrap_key=False
        ):

        if not (auth_key_filepath or auth_key):
            raise ImproperlyConfigured(
                'You must provide either an auth key or a path to a file containing the auth key'
            )

        if not auth_key:
            try:
                with open(auth_key_filepath, "r") as f:
                    auth_key = f.read()

            except Exception as e:
                raise ImproperlyConfigured("The APNS auth key file at %r is not readable: %s" % (auth_key_filepath, e))

        validate_private_key(auth_key)
        if wrap_key:
            auth_key = wrap_private_key(auth_key) # Some have had issues with keys that aren't wrappd to 64 lines

        self.team_id = team_id
        self.bundle_id = bundle_id
        self.auth_key = auth_key
        self.auth_key_id = auth_key_id
        self.force_proto = force_proto
        self.host = SANDBOX_HOST if use_sandbox else PRODUCTION_HOST

    def send_message(self, registration_id, alert, **kwargs):
        return self._send_message(registration_id, alert, **kwargs)

    def send_bulk_message(self, registration_ids, alert, **kwargs):
        good_registration_ids = []
        bad_registration_ids = []

        with closing(self._create_connection()) as connection:
            auth_token = self._get_token()

            for registration_id in registration_ids:
                try:
                    res = self._send_message(registration_id, alert, connection=connection, auth_token=auth_token, **kwargs)
                    good_registration_ids.append(registration_id)
                except:
                    bad_registration_ids.append(registration_id)

        if not bad_registration_ids:
            return res

        elif not good_registration_ids:
            raise BadDeviceToken("None of the registration ids were accepted"
                                 "Rerun individual ids with ``send_message()``"
                                 "to get more details about why")

        else:
            raise PartialBulkMessage(
                "Some of the registration ids were accepted. Rerun individual "
                "ids with ``send_message()`` to get more details about why. "
                "The ones that failed: \n:"
                "{bad_string}\n"
                "The ones that were pushed successfully: \n:"
                "{good_string}\n".format(
                    bad_string="\n".join(bad_registration_ids),
                    good_string = "\n".join(good_registration_ids)
                ),
                bad_registration_ids
            )

    def get_token_from_cache(self):
        """Do not use cache by default, just provide the function to be easily overridden"""
        return None

    def set_token_to_cache(self, token):
        """Do not use cache by default, just provide the function to be easily overridden"""
        pass

    def _get_token(self):
        token = self.get_token_from_cache()

        if token is None:
            token = self._create_token()
            self.set_token_to_cache(token)

        return token

    def _create_connection(self):
        return HTTP20Connection(self.host, force_proto=self.force_proto)

    def _create_token(self):
        token = jwt.encode(
            {
                'iss': self.team_id,
                'iat': time.time()
            },
            self.auth_key,
            algorithm= ALGORITHM,
            headers={
                'alg': ALGORITHM,
                'kid': self.auth_key_id,
            }
        )

        if isinstance(token, bytes):
            token = token.decode('ascii')

        return token

    def _send_message(self, registration_id, alert, 
            badge=None, sound=None, category=None, content_available=False,
            mutable_content=False,
            action_loc_key=None, loc_key=None, loc_args=[], extra={}, 
            identifier=None, expiration=None, priority=10, 
            connection=None, auth_token=None, bundle_id=None, topic=None, push_type='alert'
        ):
        topic = topic or bundle_id or self.bundle_id
        if not topic:
            raise ImproperlyConfigured(
                'You must provide your bundle_id if you do not specify a topic'
            )

        if push_type not in APNS_PUSH_TYPES:
            raise InvalidPushType('The push-type provided is not valid')

        if push_type == 'voip' and not topic.endswith('.voip'):
            raise BadTopic('Topic should be in the format <bundle_id>.voip when using voip push_type')

        data = {}
        aps_data = {}

        if action_loc_key or loc_key or loc_args:
            alert = {"body": alert} if alert else {}
            if action_loc_key:
                alert["action-loc-key"] = action_loc_key
            if loc_key:
                alert["loc-key"] = loc_key
            if loc_args:
                alert["loc-args"] = loc_args

        if alert is not None:
            aps_data["alert"] = alert

        if badge is not None:
            aps_data["badge"] = badge

        if sound is not None:
            aps_data["sound"] = sound

        if category is not None:
            aps_data["category"] = category

        if content_available:
            aps_data["content-available"] = 1

        if mutable_content:
            aps_data["mutable-content"] = 1

        data["aps"] = aps_data
        data.update(extra)

        # Convert to json, avoiding unnecessary whitespace with separators (keys sorted for tests)
        json_data = json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")

        if len(json_data) > MAX_NOTIFICATION_SIZE:
            raise PayloadTooLarge("Notification body cannot exceed %i bytes" % (MAX_NOTIFICATION_SIZE))

        # If expiration isn't specified use 1 month from now
        expiration_time = expiration if expiration is not None else int(time.time()) + 2592000

        auth_token = auth_token or self._get_token()

        request_headers = {
            'apns-expiration': str(expiration_time),
            'apns-id': str(identifier or uuid.uuid4()),
            'apns-priority': str(priority),
            'apns-topic': topic,
            'apns-push-type': push_type,
            'authorization': 'bearer {0}'.format(auth_token)
        }

        if connection:
            response = self._send_push_request(connection, registration_id, json_data, request_headers)
        else:
            with closing(self._create_connection()) as connection:
                response = self._send_push_request(connection, registration_id, json_data, request_headers)

        return response

    def _send_push_request(self, connection, registration_id, json_data, request_headers):
        connection.request(
            'POST', 
            '/3/device/{0}'.format(registration_id), 
            json_data, 
            headers=request_headers
        )
        response = connection.get_response()

        if response.status != APNSResponse.Success:
            body = json.loads(response.read().decode('utf-8'))
            reason = body.get("reason")

            if reason:
                exceptions_module = importlib.import_module("gobiko.apns.exceptions")
                # get exception class by name
                raise getattr(exceptions_module, reason, InternalException)

        return response
