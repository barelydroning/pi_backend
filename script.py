import sys
from socketIO_client_nexus import SocketIO, LoggingNamespace
import logging
import RPi.GPIO as GPIO
import time
from queue import Queue
from threading import Thread
import threading
import asyncio

GPIO.setmode(GPIO.BCM)

PIN_TRIGGER = 15
PIN_ECHO = 14

GPIO.setup(PIN_TRIGGER, GPIO.OUT)
GPIO.setup(PIN_ECHO, GPIO.IN)

GPIO.output(PIN_TRIGGER, False)
print('Waiting for Sensor to settle')
time.sleep(2)

#logging.getLogger('socketIO-client').setLevel()
#logging.basicConfig()


SERVER_IP = 'http://192.168.0.29'
# SERVER_IP = 'http://192.168.1.128'
SERVER_PORT = 3001

START_MSG = "START"
STOP_MSG = "STOP"

q = Queue()

def continuous_loop():
    while True:
        # get start message (blocking)
        while q.get() != START_MSG:
            pass
        while q.get_nowait() != STOP_MSG:
            distance = get_measurement()
            print('Distance is:', distance)
        
def on_connect():
    print('connect')


def on_disconnect():
    print('disconnect')


def on_reconnect():
    print('reconnect')


def on_command(data):
    _type = data['type']

    if _type == 'kill':
        GPIO.cleanup()
        sys.exit()
        print('KILL')
    elif _type == 'distance':
        distance = get_measurement()
        print('Distance is:', distance)
    elif _type == 'start_loop':
        q.put(START_MSG)
    elif _type == 'quit_loop':
        q.put(STOP_MSG)
    else:
        print('OTHER COMMAND')

def get_measurement():
    GPIO.output(PIN_TRIGGER, True)

    time.sleep(0.00001)

    GPIO.output(PIN_TRIGGER, False)

    while GPIO.input(PIN_ECHO) == 0:
        pulse_start = time.time()
    
    while GPIO.input(PIN_ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start

    distance = round(17150 * pulse_duration, 2)

    return distance


    

# get_measurement()

# while (True):
#     distance = get_measurement()
#     print('Distance is:', distance)
#     time.sleep(.05)


Thread(target=continuous_loop)
socket = SocketIO(SERVER_IP, SERVER_PORT)
socket.on('connect', on_connect)
socket.on('disconnect', on_disconnect)
socket.on('reconnect', on_reconnect)
socket.on('command', on_command)

socket.emit('connect_rover')

socket.wait()


