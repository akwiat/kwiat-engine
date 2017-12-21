from flask import Flask, render_template
from flask_socketio import SocketIO
from flask import request
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@socketio.on('message')
def handle_message(message):
	print("\nid :{}".format(request.sid))

	print("received message: {}".format(message))


@socketio.on('connect')
def test_connect(*args, **kwargs):
	print("\nid :{}".format(request.sid))
	print("user connected: {}, {}".format(args, kwargs))
    # emit('my response', {'data': 'Connected'})

if __name__ == '__main__':
    socketio.run(app)