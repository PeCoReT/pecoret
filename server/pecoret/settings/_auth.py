## django-all auth
HEADLESS_ONLY = True

# we use username field for login
ACCOUNT_AUTHENTICATION_MODE = 'username'

HEADLESS_FRONTEND_URLS = {
    'socialaccount_login_error': '/#/login',
    'account_reset_password_from_key': '/#/reset-password/{key}',
}

# custom allauth adapters
SOCIALACCOUNT_ADAPTER = 'backend.adapter.PeCoReTSocialAccountAdapter'
ACCOUNT_ADAPTER = 'backend.adapter.PeCoReTAccountAdapter'
HEADLESS_ADAPTER = 'backend.adapter.PeCoReTHeadlessAdapter'

# Configures whether password reset attempts for email addresses which do not have an account result in sending an email.
ACCOUNT_EMAIL_UNKNOWN_ACCOUNTS = False
# only allow a user to have one email address
ACCOUNT_MAX_EMAIL_ADDRESSES = 1
ACCOUNT_CHANGE_EMAIL = False
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']

# make username lowercase which prevents expensive `__iexact` lookups
ACCOUNT_PRESERVE_USERNAME_CASING = False

# Authentication
AUTH_USER_MODEL = "backend.User"
LOGIN_REDIRECT_URL = '/'

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    "django.contrib.auth.backends.ModelBackend",
)

LDAP_SYNC_GROUP_MAPPING = {}
