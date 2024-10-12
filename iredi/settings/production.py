from .base import *

DEBUG = os.getenv("DEBUG") == 'True'

SECRET_KEY = os.getenv("SECRET_KEY")

ALLOWED_HOSTS = ["*"]

try:
    from .local import * #type: ignore
except ImportError:
    pass
