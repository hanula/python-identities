
from nose.tools import assert_equal, assert_true, ok_
from identities.manager import IdentityManager
from identities.identity import Identity
from identities.providers import TokenIdentityProvider, PasswordIdentityProvider
from identities.store.sqlstore import SQLStore
from identities.store.memory import MemoryStore

class IdentityProvider(object):
    
    def __init__(self, origin, manager):
        self.origin = origin
        self.manager = manager
        
    def identify(self, verifier):
        return self.manager.store.identify(self.origin, verifier)
    
    def store_identity(self, identity):
        return self.manager.store.store(identity)
    
    def delete_identity(self, identity):
        return self.manager.store.delete(identity.id)
    
    def identity_resources(self, identity):
        self.manager.store.identity_resources(identity)
        
    def get_resource(self, resource_id):
        return None
    

class DefaultProvider(IdentityProvider):
    pass

class PasswordIdentity(IdentityProvider):
    
    def load_resource(self, resource_id):
        r = User()
        r.id = resource_id
        return r
    
    def store_identity(self, identity):
        identity.verifier = identity.verifier.encode('rot13')
        return IdentityProvider.store_identity(self, identity)


    def identify(self, verifier):
        return IdentityProvider.identify(self, verifier.decode('rot13'))


class User(object):
    def __init__(self, id):
        self.id = id
        
def assert_equal_identities(e1, e2):
    assert_equal(e1.origin, e2.origin)
    assert_equal(e1.resource_id, e2.resource_id)
    assert_equal(e1.name, e2.name)

def test_it_all_already():
    
    #manager = IdentityManager(SQLStore({'sqlalchemy.url' : 'sqlite:///:memory:'}))
    manager = IdentityManager(MemoryStore())
    
    
    user = User(123)
            
    
    manager.register_provider('external_account', IdentityProvider)
    manager.register_provider('token', TokenIdentityProvider)
    manager.register_provider('password', PasswordIdentityProvider)
    
    
    
    # Test basic identity
    test_identity = Identity('external_account', user.id, u'some_user_id', name=u"Some Username")
    assert_equal(test_identity.origin, 'external_account')
    assert_equal(test_identity.resource_id, user.id)
    assert_equal(test_identity.name, u'Some Username')
    
    # store it twice = update
    manager.store_identity(test_identity)
    id = manager.store_identity(test_identity)
    assert_equal(len(manager.get_identities(user.id)), 1)
    identity = manager.identify('external_account', u'some_user_id')
    assert_true(identity is not None)
    assert_equal_identities(identity, test_identity)
    
    identity = manager.get_identity(id)
    assert_equal_identities(identity, test_identity)
    assert_equal(len(manager.get_identities(user.id)), 1)
    
    # Test token identity
    test_identity = manager.create_identity('token', user.id)
    assert_equal(len(manager.get_identities(user.id)), 1)   # just creation, no storing
    assert_equal(test_identity.origin, 'token')
    assert_equal(test_identity.resource_id, user.id)
    assert_true(test_identity.verifier is not None)
    manager.store_identity(test_identity)
    assert_equal(len(manager.get_identities(user.id)), 2)
    
    identity = manager.identify('token', test_identity.verifier)
    assert_equal_identities(identity, test_identity)
        
    
    # Test password identity
    test_identity = manager.create_identity('password', user.id, u'somepassword')
    id = manager.store_identity(test_identity)
    identity = manager.identify('password', (user.id, u'somepassword'))
    assert_true(identity is not None)
    assert_equal_identities(identity, test_identity)    
    
    assert_equal(len(manager.get_identities(user.id)), 3)
    
    manager.remove_identity(id)
    
    assert_equal(len(manager.get_identities(user.id)), 2)
    
    
    
    
    
    