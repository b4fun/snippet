"""
tree
~~~~

Code sample for querying tree like data with CTE.
"""

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from typing import List

Base = declarative_base()


class Staff(Base):

    __tablename__ = 'staff'

    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(64), nullable=False)
    supervisor_id = sa.Column(
        sa.Integer,
        sa.ForeignKey('staff.id'),
        nullable=True,
    )
    supervisor = relationship(
        'Staff',
        backref=backref('subordinates', cascade='all, delete-orphan'),
        remote_side=[id],
        # allow circular
        post_update=True,
    )

    def __str__(self):
        supervisor = '(none)'
        if self.supervisor:
            supervisor = f'({self.supervisor.id}, {self.supervisor.name})'
        return f'<Staff id={self.id} name={self.name} supervisor={supervisor}>'

    def __repr__(self):
        return self.__str__()


def init_test_data(session):
    session.execute('truncate table staff')

    alice = Staff(name='alice')
    session.add(alice)
    bob = Staff(name='bob', supervisor=alice)
    session.add(bob)
    claire = Staff(name='claire', supervisor=alice)
    session.add(claire)
    david = Staff(name='david', supervisor=bob)
    session.add(david)
    eric = Staff(name='eric', supervisor=bob)
    session.add(eric)
    fiona = Staff(name='fiona', supervisor=claire)
    session.add(fiona)
    gabe = Staff(name='gabe', supervisor=claire)
    session.add(gabe)

    session.commit()


def init_circular_test_data(session):
    session.execute('truncate table staff')

    alice = Staff(name='alice')
    session.add(alice)
    bob = Staff(name='bob', supervisor=alice)
    session.add(bob)
    claire = Staff(name='claire', supervisor=alice)
    session.add(claire)
    david = Staff(name='david', supervisor=bob)
    session.add(david)
    eric = Staff(name='eric', supervisor=bob)
    session.add(eric)
    fiona = Staff(name='fiona', supervisor=claire)
    session.add(fiona)
    gabe = Staff(name='gabe', supervisor=claire)
    session.add(gabe)

    # reference back
    alice.supervisor = gabe

    session.commit()


def query_tree(session, supervisor_id: int) -> List[Staff]:
    _cte_base = session.query(Staff) \
        .filter(Staff.supervisor_id == supervisor_id) \
        .cte(name='staff_cte', recursive=True)
    _cte_base_alias = _cte_base.alias()

    _cte = _cte_base.union_all(
        session
        .query(Staff)
        .filter(_cte_base_alias.c.id == Staff.supervisor_id)
    )

    q = sa.select([
        _cte.c.id.label('id'),
        _cte.c.name.label('name'),
        _cte.c.supervisor_id.label('supervisor_id'),
    ])
    return session.query(Staff).from_statement(q).all()


def query_tree_with_depth_limit(
    session,
    supervisor_id: int,
    depth_limit: int,
) -> List[Staff]:
    _cte_base = sa.select([
        Staff,
        sa.sql.literal_column('1').label('depth_limit'),
    ]) \
        .where(Staff.supervisor_id == supervisor_id) \
        .cte(name='staff_cte', recursive=True)
    _cte_base_alias = _cte_base.alias()

    _cte = _cte_base.union_all(
        sa.select([
            Staff,
            (_cte_base_alias.c.depth_limit + 1).label('depth_limit'),
        ])
        .where(_cte_base_alias.c.id == Staff.supervisor_id)
        .where(_cte_base_alias.c.depth_limit < depth_limit)
    )

    q = sa.select([
        _cte.c.id.label('id'),
        _cte.c.name.label('name'),
        _cte.c.supervisor_id.label('supervisor_id'),
    ])
    return session.query(Staff).from_statement(q).all()


if __name__ == '__main__':
    import os
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # export local connection here
    # example:
    #
    #   export SNIPPET_MYSQL_CONN=mysql+pymysql://root:root@localhost:3306/test
    #
    # NOTE: require mysql 8.0+
    engine = create_engine(os.getenv('SNIPPET_MYSQL_CONN'), echo=False)
    Session = sessionmaker(bind=engine)

    # create the staff table
    Base.metadata.create_all(engine)

    init_test_data(Session())
    session = Session()

    for staff in session.query(Staff).all():
        print(staff)

    print('subordinates of id=1:')
    for staff in query_tree(session, 1):
        print(staff)

    print('-' * 20)
    print('subordinates of id=2:')
    for staff in query_tree(session, 2):
        print(staff)

    print('-' * 20)
    print('subordinates of id=4:')
    for staff in query_tree(session, 4):
        print(staff)

    session.rollback()

    init_circular_test_data(Session())
    session = Session()

    print('-' * 20)
    print('subordinates of id=1, depth=1:')
    for staff in query_tree_with_depth_limit(session, 1, 1):
        print(staff)

    print('-' * 20)
    print('subordinates of id=2, depth=1:')
    for staff in query_tree_with_depth_limit(session, 2, 1):
        print(staff)

    print('-' * 20)
    print('subordinates of id=4, depth=1:')
    for staff in query_tree_with_depth_limit(session, 4, 1):
        print(staff)
