from scribble import app
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError

conn = r.connect(host=app.config['RDB_HOST'],
                 port=app.config['RDB_PORT'])

try:
    r.db_create(app.config['RDB_DB']).run(conn)
    print "Database created"
except RqlRuntimeError:
    print "Error: database already exists"
finally:
    conn.close()
