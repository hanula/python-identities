

from identities.manager import IdentityManager
from identities.store.sqlstore import SQLStore
from identities.providers import PasswordIdentityProvider, TokenIdentityProvider
from sqlalchemy import create_engine, Column, Integer, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


# Setup ID manager with example providers
id_manager = IdentityManager()
id_manager.register_provider('password', PasswordIdentityProvider)
id_manager.register_provider('token', TokenIdentityProvider)

Base = declarative_base()
Session = scoped_session(sessionmaker())


class IdentityResourceMixin(object):
    
    def get_identities(self, origin=None):
        return id_manager.get_identities(self.id, origin)

class User(Base, IdentityResourceMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Unicode(256), unique=True, nullable=False)
    email = Column(Unicode(256), unique=True, nullable=False)
    
    def set_password(self, password):
        id_manager.add_identity('password', self.id, password)
        
    def has_password(self, password):
        return id_manager.identify('password', (self.id, password)) is not None
    
    
class Thing(Base, IdentityResourceMixin):
    __tablename__ = 'things'
    id = Column(Integer, primary_key=True)
    content = Column(Unicode(256), nullable=False)
            
    @property
    def token(self):
        ids = self.get_identities('token')
        return ids and ids[0].verifier or None
    
    def generate_token(self):
        id_manager.add_identity('token', self.id)
        return self.token
        
    @classmethod
    def get_by_token(cls, token):
        identity = id_manager.identify('token', token)
        if identity:
            return Session.query(cls).get(identity.resource_id)

# Configure Sqlalchemy
engine = create_engine('sqlite:///:memory:')
Session.configure(bind=engine)
Base.metadata.create_all(engine)
# Configure identity storage
id_manager.set_store(SQLStore(engine))

# Put some example data
user = User(username=u'Tester', email=u'tester@user.com')
thing = Thing(content=u'Some fancy content')
Session.add(user)
Session.add(thing)
Session.commit()

# test user password
user.set_password('my pass')
assert user.has_password('other') is False
assert user.has_password('my pass') is True

# Test token
print "Thing's Generated token:", thing.generate_token()
assert Thing.get_by_token(thing.token) is thing

