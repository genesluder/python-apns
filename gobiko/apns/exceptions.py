

class APNsException(Exception):
    pass


class InternalException(APNsException):
    pass


class ImproperlyConfigured(APNsException):
    pass


class BadCollapseId(APNsException):
    "The collapse identifier exceeds the maximum allowed size"
    pass


class BadDeviceToken(APNsException):
    "The specified device token was bad. Verify that the request contains a valid token and that the token matches the environment."
    pass


class BadExpirationDate(APNsException):
    "The apns-expiration value is bad."
    pass


class BadMessageId(APNsException):
    "The apns-id value is bad."
    pass


class BadPriority(APNsException):
    "The apns-priority value is bad."
    pass


class BadTopic(APNsException):
    "The apns-topic was invalid."
    pass


class DeviceTokenNotForTopic(APNsException):
    "The device token does not match the specified topic."
    pass


class DuplicateHeaders(APNsException):
    "One or more headers were repeated."
    pass


class IdleTimeout(APNsException):
    "Idle time out."
    pass


class MissingDeviceToken(APNsException):
    "The device token is not specified in the request :path. Verify that the :path header contains the device token."
    pass


class MissingTopic(APNsException):
    "The apns-topic header of the request was not specified and was required. The apns-topic header is mandatory when the client is connected using a certificate that supports multiple topics."
    pass


class PayloadEmpty(APNsException):
    "The message payload was empty."
    pass


class TopicDisallowed(APNsException):
    "Pushing to this topic is not allowed."
    pass


class BadCertificate(APNsException):
    "The certificate was bad."
    pass


class BadCertificateEnvironment(APNsException):
    "The client certificate was for the wrong environment."
    pass


class ExpiredProviderToken(APNsException):
    "The provider token is stale and a new token should be generated."
    pass


class Forbidden(APNsException):
    "The specified action is not allowed."
    pass


class InvalidProviderToken(APNsException):
    "The provider token is not valid or the token signature could not be verified."
    pass


class MissingProviderToken(APNsException):
    "No provider certificate was used to connect to APNs and Authorization header was missing or no provider token was specified."
    pass


class BadPath(APNsException):
    "The request contained a bad :path value."
    pass


class MethodNotAllowed(APNsException):
    "The specified :method was not POST."
    pass


class Unregistered(APNsException):
    "The device token is inactive for the specified topic. Expected HTTP/2 status code is 410; see Table 8-4."
    pass


class PayloadTooLarge(APNsException):
    "The message payload was too large. See Creating the Remote Notification Payload for details on maximum payload size."
    pass


class TooManyProviderTokenUpdates(APNsException):
    "The provider token is being updated too often."
    pass


class TooManyRequests(APNsException):
    "Too many requests were made consecutively to the same device token."
    pass


class InternalServerError(APNsException):
    "An internal server error occurred."
    pass


class ServiceUnavailable(APNsException):
    "The service is unavailable."
    pass


class Shutdown(APNsException):
    "The server is shutting down."
    pass

