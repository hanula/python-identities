
from datetime import datetime

class Identity(object):
    """
    Describes the identity of a resource.
    
    """
    
    def __init__(self, origin, resource_id, verifier, name=None, creation_time=None, expiration_time=None):
        self.origin = origin
        self.resource_id = resource_id
        self.verifier = verifier
        self.name = name
        self.creation_time = creation_time or datetime.now()
        self.expiration_time = expiration_time        
                
        
    def __repr__(self):
        return '<Identity: %s:%s>' % (self.resource_id, self.origin)
    