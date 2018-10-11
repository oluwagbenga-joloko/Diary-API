from decouple import config
import os

env = config("ENV", "")
if env == "development":
    from .development import *
elif env =="production":
    from .production import *
else:
    from .base import *