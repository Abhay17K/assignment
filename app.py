from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'chat_app.db')
db = SQLAlchemy(app)

# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    admin = db.relationship('User', backref='admin_of_groups')


class GroupMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='groups')


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    likes = db.relationship('Like', backref='message', cascade='all, delete-orphan')


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('message.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# Authentication APIs
@app.route('/login', methods=['POST'])
def login():
    # Handle login functionality
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username, password=password).first()

    if user:
        # Successful login
        return jsonify({'message': 'Login successful'})
    else:
        # Invalid credentials
        return jsonify({'message': 'Invalid credentials'})


@app.route('/logout', methods=['POST'])
def logout():
    # Handle logout functionality
    return jsonify({'message': 'Logout Successful'})


# Admin APIs
@app.route('/admin/users', methods=['POST'])
def create_user():
    # Create a new user (admin only)
    username = request.json.get('username')
    password = request.json.get('password')

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created'})


@app.route('/admin/users/<user_id>', methods=['PUT'])
def edit_user(user_id):
    # Edit user details (admin only)
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.get(user_id)
    if user:
        user.username = username
        user.password = password
        db.session.commit()
        return jsonify({'message': f'User {user_id} updated'})
    else:
        return jsonify({'message': f'User {user_id} not found'}), 404


# Normal User APIs
@app.route('/groups', methods=['POST'])
def create_group():
    # Create a new group
    group_name = request.json.get('group_name')
    admin_id = request.json.get('admin_id')

    group = Group(name=group_name, admin_id=admin_id)
    db.session.add(group)
    db.session.commit()

    return jsonify({'message': 'Group created'})


@app.route('/groups/<group_id>', methods=['DELETE'])
def delete_group(group_id):
    # Delete a group
    group = Group.query.get(group_id)
    if group:
        db.session.delete(group)
        db.session.commit()
        return jsonify({'message': f'Group {group_id} deleted'})
    else:
        return jsonify({'message': f'Group {group_id} not found'}), 404


@app.route('/groups/search', methods=['GET'])
def search_groups():
    # Search groups
    groups = Group.query.all()
    result = [{'id': group.id, 'name': group.name} for group in groups]
    return jsonify({'groups': result})


@app.route('/groups/<group_id>/members', methods=['POST'])
def add_member(group_id):
    # Add a member to a group
    group = Group.query.get(group_id)
    if not group:
        return jsonify({'message': f'Group {group_id} not found'}), 404

    user_id = request.json.get('user_id')

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': f'User {user_id} not found'}), 404

    group_member = GroupMember.query.filter_by(group_id=group_id, user_id=user_id).first()
    if group_member:
        return jsonify({'message': 'Member already exists in the group'}), 409

    group_member = GroupMember(group_id=group_id, user_id=user_id)
    db.session.add(group_member)
    db.session.commit()

    return jsonify({'message': f'Member added to group {group_id}'})


@app.route('/groups/<group_id>/messages', methods=['POST'])
def send_message(group_id):
    # Send a message in a group
    group = Group.query.get(group_id)
    if not group:
        return jsonify({'message': f'Group {group_id} not found'}), 404

    user_id = request.json.get('user_id')
    content = request.json.get('content')

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': f'User {user_id} not found'}), 404

    message = Message(group_id=group_id, user_id=user_id, content=content)
    db.session.add(message)
    db.session.commit()

    return jsonify({'message': f'Message sent in group {group_id}'})

@app.route('/groups/<group_id>/messages/<message_id>/likes', methods=['POST'])
def like_message(group_id, message_id):
    # Like a message in a group
    group = Group.query.get(group_id)
    if not group:
        return jsonify({'message': f'Group {group_id} not found'}), 404

    message = Message.query.get(message_id)
    if not message:
        return jsonify({'message': f'Message {message_id} not found'}), 404

    user_id = request.json.get('user_id')

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': f'User {user_id} not found'}), 404

    like = Like.query.filter_by(message_id=message_id, user_id=user_id).first()
    if like:
        return jsonify({'message': 'User already liked the message'}), 409

    like = Like(message_id=message_id, user_id=user_id)
    db.session.add(like)
    db.session.commit()

    return jsonify({'message': f'Message {message_id} liked in group {group_id}'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


