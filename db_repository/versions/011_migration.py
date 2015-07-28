from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
source = Table('source', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('name', VARCHAR(length=140)),
    Column('frequent_users', INTEGER),
)

user = Table('user', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('username', VARCHAR(length=64)),
    Column('password', VARCHAR(length=64)),
    Column('last_seen', DATETIME),
    Column('about_me', VARCHAR(length=140)),
)

Source = Table('Source', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String),
)

User = Table('User', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=64)),
    Column('password', String(length=64)),
    Column('last_seen', DateTime),
    Column('about_me', String(length=140)),
)

daily_sources = Table('daily_sources', post_meta,
    Column('researcher_id', Integer),
    Column('source_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['source'].drop()
    pre_meta.tables['user'].drop()
    post_meta.tables['Source'].create()
    post_meta.tables['User'].create()
    post_meta.tables['daily_sources'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['source'].create()
    pre_meta.tables['user'].create()
    post_meta.tables['Source'].drop()
    post_meta.tables['User'].drop()
    post_meta.tables['daily_sources'].drop()
