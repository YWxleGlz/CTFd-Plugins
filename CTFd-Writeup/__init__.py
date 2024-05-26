from .routes import plugin_blueprint
from pathlib import Path
from CTFd.utils.plugins import override_template
from CTFd.utils import config, get_config, set_config

def load(app):
    app.db.create_all() 
    app.register_blueprint(plugin_blueprint)
    dir_path = Path(__file__).parent.resolve()
    template_path = dir_path / 'templates' / 'custom-challenge.html'

    # First run initialize to enabled
    if get_config("plugin_writeup_enabled") is None:
        set_config("plugin_writeup_enabled", True)

    if get_config("plugin_writeup_enabled"):
        # Overwrite the challenge.html template only when the plugin is enabled
        override_template('challenge.html', open(template_path).read())
