
from identities.providers.interface import IdentityProvider
import random
import string

class TokenIdentityProvider(IdentityProvider):
    require_verifier = False
    default_name = u'Token'
    token_length = 32

    def generate_token(self):
        return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(self.token_length)])
    
    def create_identity(self, resource_id, verifier=None, name=None):
        verifier = verifier or self.generate_token()
        return IdentityProvider.create_identity(self, resource_id, verifier, name)
    