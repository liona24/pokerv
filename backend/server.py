from collections import defaultdict

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room,\
    leave_room, close_room

from gameplay import Room, HumanPlayer, AiPlayer

app = Flask(__name__,
            static_folder='../dist/static',
            template_folder='../dist',
            instance_relative_config=True)
app.config.from_object('settings')
app.config.from_envvar('SERVER_SETTINGS', silent=True)

socketio = SocketIO(app)

rooms = {}
# stores temporary lock events which are used to wake the gameplay thread
# access through event_storage[room_name][name]
# each 'event' consists of an threading.Event and associated data
event_storage = defaultdict(dict)


def response(status, code, msg):
    return { 'status': status, 'code': code, 'msg': msg }


def hand_finished(summary, room):
    socketio.emit('hand finished', summary, room=room)


@app.route('/', methods=[ 'GET' ])
def index():
    return render_template('index.html')


@socketio.on('playpause')
def play_pause(args):
    room = args['room']
    play = args['play']  # check if this is actually casting correctly

    try:
        if play:
            rooms[room].start_game(lambda s: hand_finished(s, room))
            return 'ok', 200, 'Game started!'
        else:
            rooms[room].stop_game()
            return response('ok',
                            200,
                            'Game will pause after this hand finished!')
    except KeyError:
        return response('err', 404, "The specified room does not exist!")


@socketio.on('move')
def move(args):

    room = args['room']
    name = args['name']

    event = event_storage[room].pop(name, None)
    if event is None:
        return response('err', 404, "It is not '%s's turn!" % name)

    event.data.update(args)
    event.set()

    return response('ok', 200, None)


@socketio.on('create')
def create(args):
    room = args['room']
    size = int(args['size'])

    blinds = (int(args['smallblind']), int(args['bigblind']))
    initstack = int(args['stacksize'])

    if room not in rooms:
        rooms[room] = Room(room, size, initstack, blinds)
        emit('message', "Created room '%s'!" % room)
        return response('ok', 200, None)

    return response('err', 404, 'The desired room is already in use!')


@socketio.on('join')
def join(args):
    room_name = args['room']
    user_name = args['user']
    player_type = args['player_type']

    try:
        room = rooms[room_name]

        typ = HumanPlayer if player_type == 'human' else AiPlayer

        player = typ(user_name,
                     room.initstack,
                     request.sid,
                     room_name,
                     socketio,
                     event_storage)

        status, errno, msg = room.join(player)

        if status == 'ok':
            join_room(room_name)
            emit('message', 'Player %s entered the table!' % user_name,
                 room=room_name)
            emit('join', { 'players': room.serialize_players() },
                 room=room_name)
        return response(status, errno, msg)

    except KeyError:
        return response('err', 404, 'This room does not exist!')


@socketio.on('leave')
def leave(args):
    room = args['room']
    user = args['user']

    if room in rooms:
        status, errno, msg = rooms[room].leave(user)
        if status == 'ok':
            leave_room(room)
            emit('message', "Player '%s' left the table!" % user, room=room)
            if rooms[room].isempty():
                del(rooms[room])
                close_room(room)
        return response(status, errno, msg)

    return response('err', 404, 'This room does not exist!')


if __name__ == '__main__':
    socketio.run(app, debug=app.config['DEBUG'])
