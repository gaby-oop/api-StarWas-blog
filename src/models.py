from flask_sqlalchemy import SQLAlchemy

# es una extencion de python para hacer bases de datos
db = SQLAlchemy()

#
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    genero = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship('Favorites', lazy=True)#se va relacionar con la tabla de favoritos

    def __repr__(self):
        return '<User %r>' % self.id

# serialize me devuelve un diccionario= obj
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "genero":self.genero,
            "is_active":self.is_active
        }

class Personajes(db.Model):
    __tablename__ = 'personajes'
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(200))
    gender = db.Column(db.String(200),nullable=False)
    color_eyes = db.Column(db.String(200), nullable=False)
    color_hair = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Personajes %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender":self.gender,
            "color_eyes":self.color_eyes,
            "color_hair":self.color_hair 
        }
class Planetas(db.Model):
    __tablename__ ='planetas'
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(200),nullable=False)
    climate = db.Column(db.String(200),nullable=False)
    population= db.Column(db.Integer,nullable=False)
    gravity = db.Column(db.Integer, nullable=False)
    orbital_period = db.Column(db.Integer, nullable=False)
    diameter = db.Column(db.String(200),nullable=False)
    rotation_period = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Planetas %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate":self.climate,
            "population":self.population,
            "gravity":self. gravity,
            "orbital_period":self.orbital_period,
            "diameter":self.diameter,
            "rotation_period":self.rotation_period
        }
class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    favorito = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id":self.id,
            "user_id":self.user_id,
            "favorito":self.favorito
        }
#user_di almacena el id del usuario cn el q se hace relacion
#fav guarda el nombre de plan y personajes  
    

