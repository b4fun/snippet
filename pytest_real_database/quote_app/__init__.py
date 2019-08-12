"""
quote_app
~~~~~~~~~

the flask application
"""

import os


from flask import Flask, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func as sql_func


db = SQLAlchemy()


class Quote(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)


api_bp = Blueprint('api', __name__)


@api_bp.route('/hello', methods=('GET', ))
def api_hello():
    quote = db.session.query(Quote).order_by(sql_func.rand()).first()
    if not quote:
        return jsonify(message='hello, world')
    return jsonify(message=quote.message)


def create_app(**configs) -> Flask:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'SQLALCHEMY_DATABASE_URI'
    )
    app.config.update(**configs)

    db.init_app(app)

    app.register_blueprint(api_bp, url_prefix='/api')

    return app
