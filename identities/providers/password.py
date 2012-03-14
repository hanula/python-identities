
from identities.providers.interface import IdentityProvider

import hmac



class PasswordIdentityProvider(IdentityProvider):
    require_verifier = True
    default_name = u'Password'
    
    DEFAULT_HASH_METHOD = 'hmac'
    HASH_SECRET = 'dgv%^gfdWGhhsweDFSdsf$$#$#__SECRET__5423gregregNdsf'
    
    def _make_password_hash(self, password, method):
        if method == 'hmac':
            if type(password) is unicode:
                password = password.encode('utf8')
            return hmac.new(self.HASH_SECRET, password).hexdigest()
        raise ValueError("Authentication hashing method '%s' not supported" % method)
    
    def make_password(self, resource_id, password, method=DEFAULT_HASH_METHOD):
        method = method.lower()
        return '%s:%s' % (method, self._make_password_hash(str(resource_id) + password, method))
    
    #def check_password(self, password):
    #    if ':' in self.password:
    #        method, hash = self.password.split(':', 1)
    #        return hash == self._make_password_hash(resource_id, password, method)
    #    return False
    
    def create_identity(self, resource_id, verifier, name=None):
        verifier = self.make_password(resource_id, verifier)
        return IdentityProvider.create_identity(self, resource_id, verifier, name)
    
    
    def identify(self, verifier):
        if type(verifier) not in (list, tuple):
            raise TypeError("Password provider requires (resource_id, password) tuple for identification.")
        resource_id, password = verifier
        verifier = self.make_password(resource_id, password)
        return IdentityProvider.identify(self, verifier)
    