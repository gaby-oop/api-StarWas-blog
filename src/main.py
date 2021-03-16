"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,Personajes,Planetas,Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    
    return generate_sitemap(app)

#query es un fun definida es para hacer consultas a una base de datos 
#user es la class cuand llamo la class va cn mayuscula /37
@app.route('/user', methods=['GET'])
def get_users():

    all_user = User.query.all()

    result = list(map(lambda x: x.serialize(), all_user))

    return jsonify(result), 200


#obtiene un solo usuarui x id
#int = q va  ser un entero 
@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    
    if user is None :
        raise APIException("usuario no registrado",status_code = 404)

    result = user.serialize()
    
    return jsonify(result), 200

@app.route('/personajes', methods=['GET'])
def get_personajes():

    person = Personajes.query.all()

    result = list(map(lambda x : x.serialize(), person))

    return jsonify(result), 200

@app.route('/personajes/<int:personajes_id>', methods=['GET'])
def get_person(personajes_id):
    
    person = Personajes.query.get(personajes_id)
    if person is None:
      raise APIException('persona no registrado',status_code=404)

    result = person.serialize()

    return jsonify(result), 200

@app.route('/planetas', methods=['GET'])
def get_planets():

    planets = Planetas.query.all()

    result = list(map(lambda x : x.serialize(), planets))

    return jsonify(result), 200

@app.route('/planetas/<int:planetas_id>', methods=['GET'])
def get_planet(planetas_id):
    
    planet = Planetas.query.get(planetas_id)
    if planet is None:
      raise APIException('planeta no registrado',status_code=404)

    result = planet.serialize()

    return jsonify(result), 200

@app.route('/favorites', methods=['GET'])
def get_favorite():

    fav = Favorites.query.all()

    result = list(map(lambda x : x.serialize(), fav))

    return jsonify(result), 200

@app.route('/users/<int:usuario_id>/favorites', methods=['GET'])
def get_favorito(usuario_id):

    fav_id = Favorites.query.filter_by(user_id = usuario_id )#filter_by = es el q me llama la columna
    result = list(map(lambda x : x.serialize(), fav_id))

    return jsonify(result), 200

#request = pedido
#post agregar 
@app.route('/users/<int:usuario_id>/favorites', methods=['POST'])
def add_favorite(usuario_id):

    request_body = request.get_json() #el diccionario 
    favorito = Favorites(user_id = request_body['user_id'],favorito=request_body['favorito'])#tiene q ser igual al mi valor
    db.session.add(favorito)
    db.session.commit()

    return jsonify("se agrego un favorito"), 200

@app.route('/favorite/<int:favorite_id>', methods=['DELETE'])
def delete_fav(favorite_id):
    fav = Favorites.query.get(favorite_id)
    if fav is None:
        raise APIException('favorite not found', status_code=404)
    db.session.delete(fav)
    db.session.commit()
 
    return jsonify("Se elimino un favorito"), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

