from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET'])
def messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()

    messages_json = [message.to_dict() for message in messages]
    return make_response(jsonify(messages_json), 200)
    

@app.route('/messages/<int:id>', methods=['GET'])
def messages_by_id(id):
    message = db.session.get(Message, id)

    if message:
        return make_response(jsonify(message.to_dict()), 200)
    else:
        return make_response(jsonify({'error': 'Message not found'}),404)

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    
    if not data or 'body' not in data or 'username' not in data:
        return make_response(jsonify({'error': 'Missing body or username'}), 400)
    new_message = Message(body=data['body'], username=data['username'])
    db.session.add(new_message)
    db.session.commit()
    return make_response(jsonify(new_message.to_dict()), 201)  
    
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = db.session.get(Message, id)

    if not message:
        return make_response(jsonify({'error': 'Message not found'}), 404)

    data = request.get_json()
    
    if data and 'body' in data:
        message.body = data['body']
    if data and 'username' in data:
        message.username = data['username']

    db.session.commit()
    return make_response(jsonify(message.to_dict()), 200)

    
    
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)

    if not message:
        return make_response(jsonify({ 'error': 'Message not found' }), 404)
    
    db.session.delete(message)
    db.session.commit()
    return make_response(jsonify({'success':'Message deleted successfully'})), 204
    

if __name__ == '__main__':
    app.run(port=5555)
