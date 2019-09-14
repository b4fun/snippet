import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Quote(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text)


def create_app(**configs) -> Flask:
    app = Flask(__name__)

    sqlalchemy_db_url = os.getenv('SQLALCHEMY_DATABASE_URI') or 'sqlite:///'
    app.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_db_url
    app.config.update(**configs)

    db.init_app(app)

    return app


if __name__ == '__main__':
    app = create_app()
    db.create_all()
