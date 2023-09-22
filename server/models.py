from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

# Create a SQLAlchemy instance with custom naming conventions
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Define a Bakery model
class Bakery(db.Model, SerializerMixin):
    # Set the table name for this model
    __tablename__ = 'bakeries'

    # Define serialization rules for this model
    serialize_rules = ('-baked_goods.bakery',)

    # Define attributes for the Bakery model
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Create a relationship with the BakedGood model and set a back reference
    baked_goods = db.relationship('BakedGood', backref='bakery')

    # Define a human-readable representation for this model
    def __repr__(self):
        return f'<Bakery {self.name}>'

# Define a BakedGood model
class BakedGood(db.Model, SerializerMixin):
    # Set the table name for this model
    __tablename__ = 'baked_goods'

    # Define serialization rules for this model
    serialize_rules = ('-bakery.baked_goods',)

    # Define attributes for the BakedGood model
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, unique=True)
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Create a foreign key relationship with the Bakery model
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id', name='fk_baked_goods_bakery_id_bakeries'))

    # Define a human-readable representation for this model
    def __repr__(self):
        return f'<Baked Good {self.name}, ${self.price}>'