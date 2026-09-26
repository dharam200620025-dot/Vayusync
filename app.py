from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__, template_folder='.')
app.config['SECRET_KEY'] = 'vayu_sync_super_secret'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

# 1. Jab koi naya user room join karega
@socketio.on('join_chat_room')
def on_join(data):
    username = data['name']
    room = data['roomCode']
    
    join_room(room) # User ko specific room me daal diya
    
    # Us room ke sabhi logo ko batao ki koi naya aaya hai
    emit('system_message', {'msg': f"{username} joined the room ⚡"}, to=room)

# 2. Jab koi message bhejega
@socketio.on('send_message')
def handle_message(data):
    room = data['roomCode']
    
    # Message sirf usi room (to=room) mein bhejo
    emit('receive_message', data, to=room)

if __name__ == '__main__':
    print("Vayu Sync - Room Server Started! 🚀")
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
