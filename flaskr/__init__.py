import os

from flask import Flask

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}


def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        UPLOAD_FOLDER=UPLOAD_FOLDER,
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

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import news
    app.register_blueprint(news.bp)
    app.add_url_rule('/', endpoint='index')

    from . import chart
    app.register_blueprint(chart.bp)

    from . import upload
    app.register_blueprint(upload.bp)

    @app.route('/test')
    def hey():
        return news.get_post(1)['p.create_date']

    return app
