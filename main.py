from flask import Flask, render_template, session, send_file, send_from_directory, request
from flask_socketio import SocketIO, send, join_room, emit, leave_room
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    username = session.get("username")
    if not username:
        return "your arent logged in"
    room = session.get("room")
    if not room:
        return "your arent in a room"
    members = rooms[room]['users']
    if username not in members:
        rooms[room]['users'].append(username)
        members.append(username)
    return render_template('index.html', room=room, members=members, username=username)


@app.route('/signin', methods=['POST'])
def signin():
    username = request.form["username"]
    password = request.form["password"]
    

    if users[username] != password:
        return "wrong username or password"


    session['username'] = username

    room = session.get("room")
    members = rooms[room]['users']
    return render_template('index.html', room=room, members=members, username=username)

@app.route('/join_room', methods=['POST'])
def join_room_route():
    room = int(request.form["room"])
    password = int(request.form["password"])

    if room not in rooms:
        return "this room does not exist"

    if rooms[room]['code'] != password:
        return "wrong password"
        
    session['room'] = room
    name = session.get("username")
    print(f"{name = }")


    return render_template('index.html')


@socketio.on('connect')
def handle_message():
    room = session.get("room")
    if not room:
        return "you are not in a room my friend"
    
    name = session.get("name")
    if name not in rooms[room]['users']:
        rooms[room]["users"].append(name)

    join_room(room, request.sid)



@socketio.on('message')
def handle_message(message):
    room = session.get('room')
    username = session.get("username")
    print('Received message:', message, "from", session.get("username"))
    current_time = datetime.now()
    hours = current_time.hour
    
    minutes = current_time.minute
    if hours < 12:
        time = f"{hours}:{0 if minutes < 10 else ''}{minutes}AM"
    else:
        time = f"{hours-12}:{0 if minutes < 10 else ''}{minutes}PM"

    send(f"{username}: {message} -- {time}", to=room) 
    # send(f"{username}: {message}", broadcast=True)

 
users = {
    "shmuli": "password",
    "dude": "hack",
    "jon": "spill",
}

rooms = {
    2827: {'code': 75, 'users': []},
    129: {'code': 26, 'users': []},
    2736: {'code': 35, 'users': []},
    23: {'code': 21, 'users': []},
}



if __name__ == '__main__':
    socketio.run(app)
