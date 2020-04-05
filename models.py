from sqlalchemy import Column, Integer, String
from pubsub import pub
from db import Base, session


class Nota(Base):
    __tablename__ = 'notas'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    title = Column(String(100))
    body = Column(String())

    def delete(self):
        session.delete(self)
        session.commit()
        pub.sendMessage('nota_deleted')

    def save(self):
        session.add(self)
        session.commit()
        pub.sendMessage('nota_saved')

    def to_tuple(self):
        return (self.id, self.title, self.body)

    def __repr__(self):
        return self.title


Base.metadata.create_all()
