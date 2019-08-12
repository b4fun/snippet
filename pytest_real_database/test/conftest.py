import pathlib
import alembic
from alembic.config import Config as AlembicConfig
import pytest

from quote_app import create_app
# the application scoped database instance
from quote_app import db as _db


_project_root = pathlib.Path(__file__).parent.parent


@pytest.fixture(scope='session')
def app(request):
    """Create flask application (session scope)."""
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
def create_db_with_alembic(app, request):
    # bind the app the database instance
    _db.app = app

    alembic_config = AlembicConfig(_project_root / 'alembic.ini')
    # override settings & run migrations
    alembic_config.set_section_option(
        'alembic', 'sqlalchemy.url',
        app.config['SQLALCHEMY_DATABASE_URI']
    )
    alembic.command.upgrade(alembic_config, 'head')

    def teardown():
        _db.session.remove()
        _db.drop_all()
        # drop alembic's revisions table, so next test can re-run these
        # migrations
        _db.session.execute('drop table if exists alembic_version')

    request.addfinalizer(teardown)

    return _db


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
def db(
    # change this parameter to use the other implementation
    create_db_with_alembic,
    # create_db_with_sqlalchemy,
    request,
):
    db = create_db_with_alembic
    # db = create_db_with_sqlalchemy

    def cleanup_tables():
        # sort tables with topology order, ensure children tables are
        # deleted first
        for table in db.metadata.sorted_tables[::-1]:
            db.session.execute(table.delete())
        db.session.commit()

    cleanup_tables()
    request.addfinalizer(cleanup_tables)

    return db


@pytest.fixture
def api_client(db, app):
    """Create api request client."""
    return app.test_client()
