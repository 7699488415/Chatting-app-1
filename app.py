from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect
from datetime import datetime
import json
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Enable CORS for all routes
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Store connected users and their session info
connected_users = {}
active_rooms = {'general': {'users': [], 'messages': []}}

class ChatUser:
    def __init__(self, username, session_id, is_guest=False):
        self.username = username
        self.session_id = session_id
        self.is_guest = is_guest
        self.joined_at = datetime.now()
        self.last_seen = datetime.now()

    def to_dict(self):
        return {
            'username': self.username,
            'session_id': self.session_id,
            'is_guest': self.is_guest,
            'joined_at': self.joined_at.isoformat(),
            'last_seen': self.last_seen.isoformat()
        }

@app.route('/')
def login():
    """Serve the login page"""
    return render_template('login.html')

@app.route('/chat')
def chat():
    """Serve the chat page"""
    return render_template('chat.html')

@app.route('/api/users')
def get_users():
    """Get list of connected users"""
    users = [user.to_dict() for user in connected_users.values()]
    return jsonify({
        'users': users,
        'count': len(users)
    })

@app.route('/api/messages')
def get_messages():
    """Get recent messages from general room"""
    messages = active_rooms['general']['messages'][-50:]  # Last 50 messages
    return jsonify({
        'messages': messages,
        'count': len(messages)
    })

# WebSocket Events
@socketio.on('connect')
def on_connect():
    """Handle client connection"""
    print(f'Client connected: {request.sid}')
    emit('connection_response', {
        'status': 'connected',
        'session_id': request.sid,
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('disconnect')
def on_disconnect():
    """Handle client disconnection"""
    session_id = request.sid
    print(f'Client disconnected: {session_id}')
    
    if session_id in connected_users:
        user = connected_users[session_id]
        username = user.username
        
        # Remove user from connected users
        del connected_users[session_id]
        
        # Remove from general room
        if username in active_rooms['general']['users']:
            active_rooms['general']['users'].remove(username)
        
        # Notify other users
        emit('user_left', {
            'username': username,
            'timestamp': datetime.now().isoformat(),
            'user_count': len(connected_users)
        }, broadcast=True)
        
        print(f'User {username} disconnected')

@socketio.on('join_chat')
def on_join_chat(data):
    """Handle user joining the chat"""
    username = data.get('username')
    is_guest = data.get('is_guest', False)
    session_id = request.sid
    
    if not username:
        emit('error', {'message': 'Username is required'})
        return
    
    # Check if username is already taken
    existing_usernames = [user.username for user in connected_users.values()]
    if username in existing_usernames:
        emit('error', {'message': 'Username is already taken'})
        return
    
    # Create user object
    user = ChatUser(username, session_id, is_guest)
    connected_users[session_id] = user
    
    # Join general room
    join_room('general')
    active_rooms['general']['users'].append(username)
    
    # Send welcome message to user
    emit('welcome', {
        'message': f'Welcome to ChatApp, {username}!',
        'username': username,
        'is_guest': is_guest,
        'timestamp': datetime.now().isoformat()
    })
    
    # Notify other users
    emit('user_joined', {
        'username': username,
        'is_guest': is_guest,
        'timestamp': datetime.now().isoformat(),
        'user_count': len(connected_users)
    }, broadcast=True, include_self=False)
    
    # Send current users list to the new user
    users_list = [{'username': u.username, 'is_guest': u.is_guest} 
                  for u in connected_users.values()]
    emit('users_list', {
        'users': users_list,
        'count': len(users_list)
    })
    
    # Send recent messages to the new user
    recent_messages = active_rooms['general']['messages'][-20:]  # Last 20 messages
    if recent_messages:
        emit('message_history', {'messages': recent_messages})
    
    print(f'User {username} joined the chat')

@socketio.on('send_message')
def on_send_message(data):
    """Handle sending a message"""
    session_id = request.sid
    
    if session_id not in connected_users:
        emit('error', {'message': 'User not authenticated'})
        return
    
    user = connected_users[session_id]
    message_text = data.get('message', '').strip()
    
    if not message_text:
        emit('error', {'message': 'Message cannot be empty'})
        return
    
    if len(message_text) > 500:
        emit('error', {'message': 'Message too long (max 500 characters)'})
        return
    
    # Create message object
    message = {
        'id': str(uuid.uuid4()),
        'username': user.username,
        'message': message_text,
        'timestamp': datetime.now().isoformat(),
        'is_guest': user.is_guest
    }
    
    # Store message in room
    active_rooms['general']['messages'].append(message)
    
    # Keep only last 100 messages to prevent memory issues
    if len(active_rooms['general']['messages']) > 100:
        active_rooms['general']['messages'] = active_rooms['general']['messages'][-100:]
    
    # Broadcast message to all users in the room
    emit('new_message', message, room='general')
    
    # Update user's last seen
    user.last_seen = datetime.now()
    
    print(f'Message from {user.username}: {message_text}')

@socketio.on('typing')
def on_typing(data):
    """Handle typing indicator"""
    session_id = request.sid
    
    if session_id not in connected_users:
        return
    
    user = connected_users[session_id]
    
    # Broadcast typing indicator to other users
    emit('user_typing', {
        'username': user.username,
        'timestamp': datetime.now().isoformat()
    }, broadcast=True, include_self=False)

@socketio.on('stop_typing')
def on_stop_typing(data):
    """Handle stop typing indicator"""
    session_id = request.sid
    
    if session_id not in connected_users:
        return
    
    user = connected_users[session_id]
    
    # Broadcast stop typing indicator to other users
    emit('user_stop_typing', {
        'username': user.username,
        'timestamp': datetime.now().isoformat()
    }, broadcast=True, include_self=False)

@socketio.on('ping')
def on_ping():
    """Handle ping for connection health check"""
    emit('pong', {'timestamp': datetime.now().isoformat()})

@socketio.on('get_user_count')
def on_get_user_count():
    """Get current user count"""
    emit('user_count', {
        'count': len(connected_users),
        'timestamp': datetime.now().isoformat()
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('login.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'connected_users': len(connected_users),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("Starting ChatApp server...")
    print("Login page: http://localhost:5000")
    print("Chat page: http://localhost:5000/chat")
    print("Health check: http://localhost:5000/health")
    
    # Run the app with SocketIO
    socketio.run(
        app, 
        host='0.0.0.0', 
        port=5000, 
        debug=True,
        allow_unsafe_werkzeug=True
    )

