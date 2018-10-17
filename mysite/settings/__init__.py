from decouple import config
import os


if config("ENV") == "development":
    from .development import *
elif config("ENV") =="production":
    from .production import *
else:
    from .base import *