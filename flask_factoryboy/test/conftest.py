import pytest

from app import create_app
from app import db as _db


@pytest.fixture(scope='session')
def app(request):
    configs = {
        'SERVER_NANE': 'test',
        'TESTING': True,
    }
    app = create_app(**configs)

    # prepare the application context
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)

    return app


@pytest.fixture(scope='session')
def create_db_with_sqlalchemy(app, request):
    # bind the app the database instance
    _db.app = app

    _db.create_all()

    def teardown():
        _db.session.remove()
        _db.drop_all()

    request.addfinalizer(teardown)

    return _db


@pytest.fixture
def db(create_db_with_sqlalchemy, request):
    db = create_db_with_sqlalchemy

    def cleanup_tables():
        # sort tables with topology order, ensure children tables are
        # deleted first
        for table in db.metadata.sorted_tables[::-1]:
            db.session.execute(table.delete())
        db.session.commit()

    cleanup_tables()
    request.addfinalizer(cleanup_tables)

    return db
