import os
from CTFd.plugins.migrations import upgrade
from CTFd.utils.plugins import override_template
from pathlib import Path
from flask import Blueprint
from .routes import plugin_blueprint

directory_name = os.path.dirname(__file__).split(os.sep)[-1] # Get the directory name of this file



def load(app):
    """
    Load the plugin into CTFd and registers the blueprint
    """

    app.register_blueprint(plugin_blueprint)

    upgrade(plugin_name="universal_flag_submitter")

    dir_path = Path(__file__).parent.resolve()
    template_path = dir_path / 'templates' / 'challenges.html'
    override_template('challenges.html', open(template_path).read())


