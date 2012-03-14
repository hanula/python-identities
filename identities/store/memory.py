

from identities.store.interface import Store

class MemoryStore(Store):
    
    def __init__(self):
        self.data = {}
        self.resource_identity_map = {}
        
    def make_id(self, origin, verifier):
        return hash(origin + verifier)
        
    def store(self, identity):
        id = self.make_id(identity.origin, identity.verifier)
        self.data[id] = identity
        self.resource_identity_map.setdefault(identity.resource_id, set()).add(id)
        return id
        
    def retrieve(self, id):
        return self.data.get(id)
    
    def remove(self, id):
        identity = self.retrieve(id)
        if identity:
            if id in self.resource_identity_map.get(identity.resource_id, []):
                self.resource_identity_map[identity.resource_id].remove(id)
            del self.data[id]
        
        
    def resource_identities(self, resource_id):
        ids = self.resource_identity_map.get(resource_id) or []
        return [self.retrieve(id) for id in ids]
    
    def identify(self, origin, verifier):
        return self.retrieve(self.make_id(origin, verifier))
    
