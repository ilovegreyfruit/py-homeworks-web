from flask import Flask, request, jsonify, abort
from datetime import datetime
from schema import AdCreateSchema, AdSchema
from pydantic import ValidationError

app = Flask(__name__)

ads = {}
ad_id_counter = 1


@app.route('/ads', methods=['POST'])
def create_ad():
    global ad_id_counter
    try:
        data = AdCreateSchema(**request.get_json())
    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400

    ad = {
        'id': ad_id_counter,
        'title': data.title,
        'description': data.description,
        'owner': data.owner,
        'created_at': datetime.utcnow()
    }

    ads[ad_id_counter] = ad
    ad_id_counter += 1
    return jsonify(ad), 201


@app.route('/ads/<int:ad_id>', methods=['GET'])
def get_ad(ad_id):
    ad = ads.get(ad_id)
    if not ad:
        abort(404, description='Ad not found')
    return jsonify(ad)


@app.route('/ads/<int:ad_id>', methods=['DELETE'])
def delete_ad(ad_id):
    ad = ads.pop(ad_id, None)
    if not ad:
        abort(404, description='Ad not found')
    return jsonify({'message': 'Ad deleted'})


@app.route('/ads/<int:ad_id>', methods=['PUT'])
def update_ad(ad_id):
    ad = ads.get(ad_id)
    if not ad:
        abort(404, description='Ad not found')

    try:
        data = request.get_json()
    except Exception:
        return jsonify({'error': 'Invalid input'}), 400

    ad['title'] = data.get('title', ad['title'])
    ad['description'] = data.get('description', ad['description'])
    ad['owner'] = data.get('owner', ad['owner'])

    return jsonify(ad)


if __name__ == '__main__':
    app.run(debug=True)