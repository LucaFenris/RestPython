from flask import Flask, jsonify, request
from client import Client
from flask_pymongo import PyMongo
from bson.objectid import ObjectId


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://172.18.0.35:27017/DBunicorn"
mongo = PyMongo(app)

#listClients = [
#        Client(name  = "Luca gordo", email = "lucagordo@gmail.com", phone = "6969696969"),
#        Client(name  = "LUUUCA gordo", email = "lucagordo1@gmail.com", phone = "69696969691"),
#        Client(name  = "LUUUUUUUUCA gordo", email = "lucagordo2@gmail.com", phone = "69696969692")
#]

@app.route('/api/v1.0/clients', methods=['GET'])
def get_tasks():
    #return "I don't believe"

    clients = []
    for c in mongo.db.clients.find():
        newClient = Client()
        newClient._id = str(c['_id'])
        newClient.name = c ['name']
        newClient.phone = c['phone']
        newClient.email = c['email']
        clients.append(newClient)
    return jsonify([c.__dict__ for c in clients]) ,201

@app.route('/api/v1.0/clients', methods=['POST'])
def create_client():
        newCli = Client()
        newCli._id = ObjectId()
        newCli.name = request.json['name']
        newCli.phone = request.json['phone']
        newCli.email = request.json['email']
        ret = mongo.db.clients.insert_one(newCli.__dict__).inserted_id
        return jsonify({'id': str(ret)}), 201

@app.route('/api/v1.0/clients/<string:_id>', methods=['PUT'])
def update_client(_id):
    updateCli = Client()
    updateCli._id = ObjectId(_id)
    updateCli.name = request.json['name']
    updateCli.phone = request.json['phone']
    updateCli.email = request.json['email']
    mongo.db.clients.update_one({'_id':updateCli._id}, {'$set':updateCli.__dict__}, upsert=False)
    return jsonify({'id': str(updateCli._id)}), 201

@app.route('/api/v1.0/clients/<string:_id>', methods=['DELETE'])
def delete_client(_id):
    _id = ObjectId(_id)
    ret = mongo.db.clients.delete_one({"_id":_id}).deleted_count
    return jsonify({'delete_count': str(ret)}), 201

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = 80)


#No método GET, toda informação é enviada para o sistema de destino junto ao endereço do sistema.
#Já o método POST, a informação é enviada de forma mais escondida e não irá aparecer na URL.
