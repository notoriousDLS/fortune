import os

from flask import Flask
from flask import render_template


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    main = Flask(__name__, instance_relative_config=True)
    main.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(main.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        main.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        main.config.update(test_config)

    # ensure the instance folder exists
    os.makedirs(main.instance_path, exist_ok=True)

    @main.route("/hello")
    def hello():
        return "Hello, World!"

    @main.route("/", endpoint="index")
    def home():
        """Public homepage. No login required."""
        return render_template("home/index.html")

    # register the database commands
    from . import db

    db.init_app(main)

    # apply the blueprints to the app
    from . import auth
    from . import blog
    from . import main

    main.register_blueprint(auth.bp)
    main.register_blueprint(blog.bp)
    main.register_blueprint(main.bp)

    return main
