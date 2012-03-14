
from identities.identity import Identity

class IdentityProvider(object):
    require_verifier = True
    default_name = None
        
    def __init__(self, origin, manager):
        self.origin = origin
        self.manager = manager
    
    def create_identity(self, resource_id, verifier, name=None):
        
        if self.require_verifier and not verifier:
            raise TypeError("verifier not specified")
        return Identity(self.origin, resource_id, verifier, name or self.default_name)
        
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
    