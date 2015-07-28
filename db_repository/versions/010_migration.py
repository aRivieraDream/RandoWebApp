from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
daily_sources = Table('daily_sources', pre_meta,
    Column('researcher', INTEGER),
    Column('source', INTEGER),
)

source = Table('source', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
    Column('frequent_users', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['daily_sources'].drop()
    post_meta.tables['source'].columns['frequent_users'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['daily_sources'].create()
    post_meta.tables['source'].columns['frequent_users'].drop()
