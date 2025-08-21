from ._apps import *
from ._base import *
from ._auth import *
from ._rest import *
from .default import *


# SECURITY WARNING: keep the secret key used in production secret!
try:
    from conf.secret_key import SECRET_KEY
except ImportError:
    # generate key
    import secrets

    with open(BASE_DIR / 'conf/secret_key.py', 'w') as f:
        secret = secrets.token_hex(132)
        f.write(f'SECRET_KEY = "{secret}"')
    SECRET_KEY = secret
