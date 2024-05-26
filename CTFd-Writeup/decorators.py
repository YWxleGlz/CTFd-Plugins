import functools
from CTFd.utils import get_config
from flask import abort

def plugin_enabled(f):
    """
    Decorator that requires the plugin enabled
    :param f:
    :return:
    """
    @functools.wraps(f)
    def plugin_enabled_wrapper(*args, **kwargs):
        if get_config("plugin_writeup_enabled"):
            return f(*args, **kwargs)
        else:
            abort(403)

    return plugin_enabled_wrapper