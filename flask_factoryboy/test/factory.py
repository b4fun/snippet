import factory

from app import db, Quote


class QuoteFactory(factory.alchemy.SQLAlchemyModelFactory):

    class Meta:
        model = Quote
        sqlalchemy_session = db.session

    author = factory.Faker('name')
    message = factory.Faker('text')
