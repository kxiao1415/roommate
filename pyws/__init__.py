from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# database connection
db = SQLAlchemy(app)

# redis connection
redis = FlaskRedis(app)

from pyws.interface import user
