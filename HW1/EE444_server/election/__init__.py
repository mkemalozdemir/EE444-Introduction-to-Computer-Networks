import os

from flask import Flask, jsonify


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'election.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from . import db
    db.init_app(app)

    from election import election_query
    app.register_blueprint(election_query.bp)
    

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(message=e.description), 404
        
    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify(message=e.description), 405
    
    @app.errorhandler(406)
    def method_not_allowed(e):
        return jsonify(message=e.description), 406

    @app.errorhandler(400)
    def method_not_allowed(e):
        return jsonify(message=e.description), 400  
    
    return app
