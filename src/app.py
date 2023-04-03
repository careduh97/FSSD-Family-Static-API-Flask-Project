"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_members():

    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def handle_post_member():

    new_member = request.json
    if new_member:
        post_member = jackson_family.add_member(new_member)
    return jsonify(post_member), 200

@app.route('/member/<int:member_id>', methods=['GET', 'DELETE'])
def handle_member_id(member_id):

    if request.method == 'GET':
        request_member = jackson_family.get_member(member_id),
        if request_member[0] == "not found":
            return jsonify({'error': 'Not found'}), 404
        return jsonify(request_member[0]), 200

    if request.method == 'DELETE':
        delete_member = jackson_family.delete_member(member_id),
        if delete_member[0] == "not found":
            return jsonify({'error': 'Not found'}), 404
        return jsonify({'done': True}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)