from socketIO_client_nexus import SocketIO, LoggingNamespace

SERVER_IP = 'http://192.168.0.29'
SERVER_PORT = 3001

def on_connect():
    print('connect')

def on_disconnect():
    print('disconnect')

def on_reconnect():
    print('reconnect')

def on_command(*args):
    print('command', args)

socket = SocketIO(SERVER_IP, SERVER_PORT)
socket.on('connect', on_connect)
socket.on('disconnect', on_disconnect)
socket.on('reconnect', on_reconnect)

socket.emit('connect_drone')

socket.on('command', on_command)

while True:
  hej = 1