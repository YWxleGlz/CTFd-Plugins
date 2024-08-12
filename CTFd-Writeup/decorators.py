import functools
from CTFd.utils import get_config
from flask import abort

def plugin_enabled(f):
    """
    Decorator to prevent access to a route if the plugin is disabled
    """
    @functools.wraps(f)
    def plugin_enabled_wrapper(*args, **kwargs):
        if get_config("plugin_writeup_enabled"):
            return f(*args, **kwargs)
        else:
            abort(403)

    return plugin_enabled_wrapper