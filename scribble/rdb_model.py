import rethinkdb as r
from scribble import app


def db_connect():
    """Return the RethinkDB connection context manager object"""
    return r.connect(host=app.config['RDB_HOST'],
                     port=app.config['RDB_PORT'],
                     db=app.config['RDB_DB'])


class Model(object):
    """
    RethinkDB-backed base model class.

    """

    # Class variables

    _table = None

    _doc = dict()

    # Magic methods

    def __init__(self, doc_id=None, doc=None):
        """
        Instantiate an object. The object can be initialized with an id to
        trigger a read (load from the database) or initialized with a
        document (using the **doc** named argument). While you can specify
        both parameters, in practice they're mutually exclusive.

        """
        if doc is not None:
            self.__dict__['_doc'] = doc
        if doc_id is not None:
            self.read(doc_id)

    def __repr__(self):
        if 'id' in self._doc:
            return "<{0} {1}>".format(type(self).__name__, self.id)
        else:
            return "<{0} (new)>".format(type(self).__name__)

    def __getattr__(self, item):
        return self._doc[item]

    def __setattr__(self, key, value):
        if key in self.__dict__:
            self.__dict__[key] = value
        else:
            self._doc[key] = value

    def __delattr__(self, item):
        del self._doc[item]

    # Instance CRUD methods

    def create(self, doc=None):
        """Insert a new model into the database. Returns generated ID."""
        if doc is None:
            doc = self._doc
        with db_connect() as conn:
            result = r.table(self._table).insert(doc).run(conn)
            if result['inserted'] == 1:
                doc_id = result['generated_keys'][0]
                self.id = doc_id
                return doc_id
            else:
                return None

    def read(self, doc_id):
        """Load the given document id."""
        with db_connect() as conn:
            self.__dict__['_doc'] = r.table(self._table).get(doc_id).run(conn)
            return self._doc

    def update(self, doc=None):
        """
        Update an existing model in the database. Returns the count of
        updated documents.

        """
        if doc is None:
            doc = self._doc
        with db_connect() as conn:
            result = r.table(self._table).get(self.id).update(doc).run(conn)
            return result.get('modified', 0) == 1

    def save(self):
        """Calls **update** or **insert** as appropriate."""
        if self._doc.has_key('id'):
            self.update()
        else:
            self.create()

    def delete(self):
        """Deletes the associated model."""
        with db_connect() as conn:
            result = r.table(self._table).get(self.id).delete().run(conn)
            ok = result.get('deleted', 0) == 1
            if ok:
                del self.id
            return ok

    # Class methods for returning sets

    @classmethod
    def __hydrate(cls, set_in):
        """Transform a list of dictionaries into a list of model objects."""

        def make_obj(x):
            obj = cls(doc=x)
            return obj

        return [make_obj(s) for s in set_in]

    @classmethod
    def read_set(cls, *args, **kwargs):
        """Read a set of document ids. Returns a list of model objects."""
        hydrate = kwargs.pop('hydrate', True)
        with db_connect() as conn:
            set = r.table(cls._table).get_all(*args, **kwargs).run(conn)
        if hydrate:
            set = cls.__hydrate(set)
        return set

    @classmethod
    def all(cls, hydrate=True):
        """Return all the objects stored for a given model."""
        with db_connect() as conn:
            set = r.table(cls._table).run(conn)
        if hydrate:
            set = cls.__hydrate(set)
        return set

    @classmethod
    def between(cls, *args, **kwargs):
        """Get all documents between two keys."""
        hydrate = kwargs.pop('hydrate', True)
        with db_connect() as conn:
            set = r.table(cls._table).between(*args, **kwargs).run(conn)
        if hydrate:
            set = cls.__hydrate(set)
        return set

    @classmethod
    def filter(cls, *args, **kwargs):
        """Get all objects for which the given predicate is true."""
        hydrate = kwargs.pop('hydrate', True)
        with db_connect() as conn:
            set = r.table(cls._table).filter(*args, **kwargs).run(conn)
        if hydrate:
            set = cls.__hydrate(set)
        return set

    @classmethod
    def r(cls):
        """Return the RethinkDB table object for this table."""
        return r.table(cls._table)
