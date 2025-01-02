from .base import *

STATIC_ROOT = "/data/local/static"
MEDIA_ROOT = "/data/local/media"

COMPRESS_OFFLINE = False

INSTALLED_APPS += [
    'shibboleth',
]

MIDDLEWARE += [
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'shibboleth.middleware.ShibbolethRemoteUserMiddleware',
]

DEBUG = False

WAGTAILUSERS_PASSWORD_REQUIRED = False

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.RemoteUserBackend',
    'shibboleth.backends.ShibbolethRemoteUserBackend',
)

SHIBBOLETH_ATTRIBUTE_MAP = {
    "OIDC_CLAIM_uid": (True, "username"),
    "OIDC_CLAIM_given_name": (True, "first_name"),
    "OIDC_CLAIM_family_name": (True, "last_name"),
}

# Do not create a new user by default upon authentication via shibboleth
CREATE_UNKNOWN_USER = False

LOGIN_URL = '/Shibboleth.sso/Login?forceAuthn=true'
#LOGIN_URL = '/OIDC.sso/redirect_uri?iss=https%3A%2F%2Fuchicago.okta.com&target_link_uri=https%3A%2F%2Fresearchdata-test.lib.uchicago.edu%2Fauthtest%2F'

SHIBBOLETH_LOGOUT_URL = 'https://shibboleth2.uchicago.edu/idp/logout.html?target=%s'

try:
    from .local import *
except ImportError:
    pass
