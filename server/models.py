from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    serialize_rules = ('-created_at', '-updated_at', '-appearances', '-guests')

    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    appearances = db.relationship('Appearance', backref = 'episode', cascade="all,delete, delete-orphan")
    guests = association_proxy('appearances', 'guest')

class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    serialize_rules = ('-created_at', '-updated_at', '-appearances', '-episodes')

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    appearances = db.relationship('Appearance', backref = 'guest')
    episodes = association_proxy('appearances', 'episode')

class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    serialize_rules = ('-created_at', '-updated_at', '-episodes', '-guests')

    id = db.Column(db.Integer, primary_key = True)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'))
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'))
    rating = db.Column(db.Integer, nullable = False)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    @validates('rating')
    def validate_rating(self, key, value):
        if value < 1 or value > 5:
            raise ValueError('Rating must be between 1 and 5')
        return value