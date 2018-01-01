from flask import Flask, Blueprint

latest = Blueprint('latest', __name__)


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config_name)

    # treat /some/url/ and /some/url the same
    app.url_map.strict_slashes = False


    from pyws.data.base_data import db
    # db connection
    db.init_app(app)

    from pyws.service.cache.cache_service import redis
    # redis connection
    redis.init_app(app, decode_responses=True)

    # server-level interface
    from pyws.interface import request_life_cycle

    # app lever interface
    from pyws.interface import user

    app.register_blueprint(latest)

    return app
