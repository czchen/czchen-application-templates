from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa


db = SQLAlchemy(metadata=sa.MetaData(
    # make sure alembic migrate will be fine
    naming_convention={
        'ix': 'ix_%(column_0_label)s',
        'uq': 'uq_%(table_name)s_%(column_0_name)s',
        'ck': 'ck_%(table_name)s_%(constraint_name)s',
        'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
        'pk': 'pk_%(table_name)s'
    }
))


class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, server_default='')
