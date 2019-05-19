from socketIO_client_nexus import SocketIO, LoggingNamespace
import logging

logging.getLogger('socketIO-client').setLevel(logging.DEBUG)
logging.basicConfig()


SERVER_IP = 'http://192.168.0.29'
SERVER_PORT = 3001


def on_connect():
    print('connect')


def on_disconnect():
    print('disconnect')


def on_reconnect():
    print('reconnect')


def on_command(data):
    _type = data['type']

    if _type == 'kill':
        print('KILL')
    else:
        print('OTHER COMMAND')


socket = SocketIO(SERVER_IP, SERVER_PORT)
socket.on('connect', on_connect)
socket.on('disconnect', on_disconnect)
socket.on('reconnect', on_reconnect)
socket.on('command', on_command)

socket.emit('connect_drone')

socket.wait()
