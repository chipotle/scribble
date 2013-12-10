from rdb_model import *
from scribble import bcrypt


class User(Model):
    _table = 'users'

    def __setattr__(self, key, value):
        """Store hash of password instead of text."""
        if key == 'password':
            value = bcrypt.generate_password_hash(value)
        super(User, self).__setattr__(key, value)

    def check_password(self, password):
        """Check password against hash, returning true on match."""
        return bcrypt.check_password_hash(self.password, password)


class Item(Model):
    _table = 'items'
