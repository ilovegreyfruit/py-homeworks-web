from flask import Flask, request, jsonify, abort
from datetime import datetime

app = Flask(__name__)

ads = {}
ad_id_counter = 1

@app.route('/ads', methods=['POST'])
def create_ad():
    global ad_id_counter

    data = request.get_json()
    required_fields = ['title', 'description', 'owner']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing fields'}), 400

    ad = {
        'id': ad_id_counter,
        'title': data['title'],
        'description': data['description'],
        'created_at': datetime.utcnow().isoformat(),
        'owner': data['owner']
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

    data = request.get_json()
    ad.update({
        'title': data.get('title', ad['title']),
        'description': data.get('description', ad['description']),
        'owner': data.get('owner', ad['owner']),
    })

    return jsonify(ad)

if __name__ == '__main__':
    app.run(debug=True)