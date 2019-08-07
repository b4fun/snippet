"""
hybrid_field
~~~~~~~~~~~~

Code sample for reading/querying JSON data with SQLAlchemy's hybrid attributes
extension.
"""

import json
from typing import Optional

import sqlalchemy as sa
from sqlalchemy import func as sa_func
from sqlalchemy.dialects import mysql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property


Base = declarative_base()


class Product(Base):

    __tablename__ = 'product'

    id = sa.Column(sa.Integer, primary_key=True)
    sku = sa.Column(sa.String(128), unique=True)
    _attributes = sa.Column('attributes', mysql.MEDIUMTEXT)

    @hybrid_property
    def attributes(self) -> dict:
        """Hybrid property for reading product attributes JSON dict.

        It always returns a dict.
        """
        if self._attributes is None:
            # null value from db side, return an empty dict
            return {}
        try:
            return json.loads(self._attributes)
        except Exception:
            # parse failed, return an empty dict
            return {}

    @hybrid_property
    def color(self) -> Optional[str]:
        """Hybrid property for reading color value from attributes JSON dict.
        """
        return self.attributes.get('color')

    @color.expression
    def color(cls):
        """SQL expression for querying color value in mysql."""
        field = sa_func.json_extract(cls._attributes, '$.color')
        return sa_func.json_unquote(field)

    @hybrid_property
    def size(self) -> Optional[str]:
        """Hybrid property for reading size value from attributes JSON dict.
        """
        return self.attributes.get('size')

    @size.expression
    def size(cls):
        """SQL expression for querying size value in mysql."""
        field = sa_func.json_extract(cls._attributes, '$.size')
        return sa_func.json_unquote(field)


if __name__ == '__main__':
    import os
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # export local connection here
    # example:
    #
    #   export SNIPPET_MYSQL_CONN=mysql+pymysql://root:root@localhost:3306/test
    engine = create_engine(os.getenv('SNIPPET_MYSQL_CONN'), echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    # reading data
    print('all products:')
    for product in session.query(Product).all():
        print(f'sku={product.sku}\tsize={product.size}\tcolor={product.color}')

    # querying records
    yellow_products = (session.query(Product)
                       .filter(Product.color == 'yellow')
                       .all())
    print('\nyellow products:')
    for product in yellow_products:
        print(f'sku={product.sku}\tsize={product.size}\tcolor={product.color}')

    lg_products = (session.query(Product)
                   .filter(Product.size == 'lg')
                   .all())
    print('\nlarge size products:')
    for product in lg_products:
        print(f'sku={product.sku}\tsize={product.size}\tcolor={product.color}')
