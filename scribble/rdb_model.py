import itertools
import rethinkdb as r
from scribble import app


def db():
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

    def __init__(self, doc=None, id=None):
        """
        Instantiate an object. The object can be initialized with an id to
        trigger a read (load from the database) or initialized with a
        document (using the **doc** named argument). While you can specify
        both parameters, in practice they're mutually exclusive.

        """
        if doc is not None:
            self.__dict__['_doc'] = doc
        if id is not None:
            self.read(id)

    def __repr__(self):
        """Printable representation of a model object."""
        if 'id' in self._doc:
            return "<{0} {1}>".format(type(self).__name__, self.id)
        else:
            return "<{0} (new)>".format(type(self).__name__)

    def __getattr__(self, item):
        """Allow retrieving document values as object properties."""
        return self._doc[item]

    def __setattr__(self, key, value):
        """Allow setting document values through object properties."""
        if key in self.__dict__:
            self.__dict__[key] = value
        else:
            self._doc[key] = value

    def __delattr__(self, item):
        """Allow deleting document values via object properties."""
        del self._doc[item]

    # Instance CRUD methods

    def create(self, doc=None):
        """Insert a new model into the database. Returns generated ID."""
        if doc is None:
            doc = self._doc
        result = r.table(self._table).insert(doc).run(db())
        if result['inserted'] == 1:
            doc_id = result['generated_keys'][0]
            self.id = doc_id
            return doc_id
        else:
            return None

    def read(self, doc_id):
        """Load the given document id."""
        self.__dict__['_doc'] = r.table(self._table).get(doc_id).run(db())
        return self._doc

    def update(self, doc=None):
        """
        Update an existing model in the database. Returns the count of
        updated documents.

        """
        if doc is None:
            doc = self._doc
        result = r.table(self._table).get(self.id).update(doc).run(db())
        return result.get('modified', 0) == 1

    def save(self):
        """Calls **update** or **insert** as appropriate."""
        if self._doc.has_key('id'):
            self.update()
        else:
            self.create()

    def delete(self):
        """Deletes the associated model."""
        result = r.table(self._table).get(self.id).delete().run(db())
        ok = result.get('deleted', 0) == 1
        if ok:
            del self.id
        return ok

    # Class methods

    @classmethod
    def has(cls, key, value):
        """
        Return true if the table contains the given key/value pair. The key
        must be an indexed column. Ex: User.has('username', 'chipotle')
        """
        doc_set = (r.table(cls._table).get_all(value, index=key).
                   limit(1).run(db()))
        return len(list(doc_set)) == 1


    @classmethod
    def read_set(cls, *args, **kwargs):
        """Read a set of documents. Returns a ModelIter object."""
        doc_set = r.table(cls._table).get_all(*args, **kwargs).run(db())
        return ModelIter(cls, doc_set)

    @classmethod
    def all(cls, hydrate=True):
        """Return all the objects stored for a given model."""
        doc_set = r.table(cls._table).run(db())
        return ModelIter(cls, doc_set)

    @classmethod
    def between(cls, *args, **kwargs):
        """Get all documents between two keys."""
        with db() as conn:
            doc_set = r.table(cls._table).between(*args, **kwargs).run(conn)
        return ModelIter(cls, doc_set)

    @classmethod
    def filter(cls, *args, **kwargs):
        """Get all objects for which the given predicate is true."""
        doc_set = r.table(cls._table).filter(*args, **kwargs).run(db())
        return ModelIter(cls, doc_set)

    @classmethod
    def r(cls):
        """Return the RethinkDB table object for this table."""
        return r.table(cls._table)


class ModelIter(object):
    """
    Wrap a RethinkDB cursor object in an iterable that will return our model
    objects when accessed.

    """
    def __init__(self, cls, cursor):
        self.cls = cls
        self.cursor = cursor

    def __iter__(self):
        for rdb in self.cursor:
            yield self.cls(doc=rdb)

    def __getitem__(self, item):
        try:
            return self.cls(doc=next(
                itertools.islice(self.cursor, item, item + 1)))
        except TypeError:
            return list(self.cls(doc=
                itertools.islice(self.cursor, item.start,
                                 item.stop, item.step)))
