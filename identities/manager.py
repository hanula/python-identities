
from identities.store.memory import MemoryStore
from identities.store.sqlstore import SQLStore
from identities.identity import Identity

class IdentityManager(object):
    """
    Manages identites and connects them with resources. 
    """
    
    def __init__(self, store=None):
        self.providers = {}
        self.store = store

    
    def register_provider(self, origin, provider):
        self.providers[origin] = provider(origin, self)
    
    def get_provider(self, origin):
        return self.providers[origin]
    
    def identify(self, origin, verifier, *args):
        """Finds identity based on the verifier."""
        #if origin in self.providers:
        return self.providers[origin].identify(verifier)
    
    def get_identity(self, id):
        return self.store.retrieve(id)
    
    def get_identities(self, resource_id):
        identities = self.store.resource_identities(resource_id)
        return identities

    def store_identity(self, identity):
        return self.get_provider(identity.origin).store_identity(identity)
    
    def create_identity(self, origin, resource_id, verifier=None, name=None):
        identity = self.get_provider(origin).create_identity(resource_id, verifier, name)
        return identity
    
    def add_identity(self, origin, resource_id, verifier=None, name=None):
        identity = self.create_identity(origin, resource_id, verifier, name)
        return self.store_identity(identity)
    
    def remove_identity(self, id):
        return self.store.remove(id)