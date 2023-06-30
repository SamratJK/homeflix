import os

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'video.sqlite')
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/test")
    def test():
        return "working"

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import videos
    app.register_blueprint(videos.bp)
    app.add_url_rule("/", endpoint="index")

    return app
