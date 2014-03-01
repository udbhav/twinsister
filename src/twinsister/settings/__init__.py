try:
    from twinsister.settings.local import *
except ImportError:
    from twinsister.settings.production import *
