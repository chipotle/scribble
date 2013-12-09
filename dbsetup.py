import argparse
from scribble import app
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError

def seed_tables():
    db.table('users').insert([
        {
            'username': 'admin',
            'display_name': 'Administrator User',
            'email': 'admin@scribble.com',
        },
        {
            'username': 'chipotle',
            'display_name': 'Watts Martin',
            'email': 'layotl@gmail.com',
            'social': { 'twitter': 'chipotlecoyote' }
        }
    ]).run(conn)
    print "+ tables seeded"

parser = argparse.ArgumentParser(description="Set up Scribble's database")
parser.add_argument('--reset', dest='reset', action='store_true', help='reset existing database')
parser.add_argument('--empty', dest='empty', action='store_true', help='do not load seed data')

args = parser.parse_args()

conn = r.connect(host=app.config['RDB_HOST'],
                 port=app.config['RDB_PORT'])

dbname = app.config['RDB_DB']

try:
    r.db_create(dbname).run(conn)
    print "+ database '{0}' created".format(dbname)
except RqlRuntimeError:
    if args.reset:
        r.db_drop(dbname).run(conn)
        print "- database dropped"
        r.db_create(dbname).run(conn)
        print "+ database '{0}' created".format(dbname)
    else:
        print "! database '{0}' already exists".format(dbname)
        exit(1)

db = r.db(dbname)

db.table_create('users').run(conn)
db.table('users').index_create('username').run(conn)
print "+ table 'users' created"

db.table_create('items').run(conn)
db.table('items').index_create('slug').run(conn)
db.table('items').index_create('type').run(conn)
db.table('items').index_create('kind').run(conn)
print "+ table 'items' created"

if args.empty:
    print "- skipping table seeding"
else:
    seed_tables()

conn.close()
