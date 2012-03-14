
from sqlalchemy import engine_from_config
from sqlalchemy.sql import select, delete
from sqlalchemy.ext.declarative import declarative_base, Column
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import Integer, Unicode, String, DateTime

Base = declarative_base()
Session = scoped_session(sessionmaker())

from identities.store.interface import Store
from identities.identity import Identity

class IdentityObject(Base, Identity):
    __tablename__ = 'identities'
    id = Column(Integer, primary_key=True)
    origin = Column(String(64), index=True)
    resource_id = Column(Integer, index=True)
    verifier = Column(String(1024), index=True)
    name = Column(Unicode(128))
    creation_time = Column(DateTime)
    expiration_time = Column(DateTime)


CONFIG = {'sqlalchemy.url' : 'sqlite:///:memory:'}



class SQLStore(Store):
    
    def __init__(self, engine):
        self.engine = engine
        Session.configure(bind=self.engine)
        Base.metadata.create_all(self.engine)
        
    def store(self, identity):
        obj = IdentityObject(origin=identity.origin, resource_id=identity.resource_id, 
                             verifier=identity.verifier, name=identity.name,
                             creation_time=identity.creation_time, expiration_time=identity.expiration_time)
        Session.add(obj)
        Session.commit()
        return obj.id
        
    def retrieve(self, id):
        return Session.query(IdentityObject).get(id)
    
    def remove(self, id):
        Session.delete(id)
        
    def resource_identities(self, resource_id, origin=None):
        query = Session.query(IdentityObject).filter_by(resource_id=resource_id)
        if origin:
            query = query.filter_by(origin=origin)
        return query.all()
    
    def identify(self, origin, verifier):
        return Session.query(IdentityObject).filter_by(origin=origin).filter_by(verifier=verifier).first()
    
