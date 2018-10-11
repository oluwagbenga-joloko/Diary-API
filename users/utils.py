import uuid
from calendar import timegm
from datetime import datetime

from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model


def jwt_payload_handler(user):
    username_field = get_user_model().USERNAME_FIELD
    username = user.get_username()


    payload = {
        'user_id': user.pk,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = str(user.pk)

    payload[username_field] = username

    # Include original issued at time for a brand new token,
    # to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    return payload


def jwt_get_username_from_payload_handler(payload):
    """
    Override this function if username is formatted differently in payload
    """
    user_name_field = get_user_model().USERNAME_FIELD
    return payload.get(user_name_field)