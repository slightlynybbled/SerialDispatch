import serial
import serialdispatch
import time
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

# the timeout keeps the serial port polling appropriately
port = serial.Serial('COM18', 57600, timeout=0.1)

# a serial port must be supplied to SerialDispatch
sd = serialdispatch.SerialDispatch(port)


def messages_received_subscriber():
    messages_received = sd.get('received')
    print('\nuc processed: {}'.format(messages_received))


def string_subscriber():
    data = sd.get('string')
    print('string received: ', data)


def i_subscriber():
    # the data is retrieved by topic
    data = sd.get('i')
    print('i received: ', data)


def array_subscriber():
    data = sd.get('array')
    print('array received: ', data)


def arrays8_subscriber():
    data = sd.get('arrays8')
    print('array8 received: ', data)


def arrays16_subscriber():
    data = sd.get('arrays16')
    print('array16 received: ', data)


def arrays32_subscriber():
    data = sd.get('arrays32')
    print('array32 received: ', data)

    
sd.subscribe('received', messages_received_subscriber)
sd.subscribe('string', string_subscriber)
sd.subscribe('i', i_subscriber)
sd.subscribe('array', array_subscriber)
sd.subscribe('arrays8', arrays8_subscriber)
sd.subscribe('arrays16', arrays16_subscriber)
sd.subscribe('arrays32', arrays32_subscriber)

i = 0
interval = 0.005
while True:
    sd.publish('received', ' ')
    sd.publish('string', 'data')
    sd.publish('i', i, ['U16'])
    sd.publish('array', [-1, -2, -3, -4], 'S16')
    sd.publish('arrays8', [[-1, -2, -3, -4], [1, 2, 3, 4]], ['S8', 'U8'])
    sd.publish('arrays16', [[-1, -2, -3, -4], [1, 2, 3, 4]], ['S16', 'U16'])
    sd.publish('arrays32', [[-1, -2, -3, -4], [1, 2, 3, 4]], ['S32', 'U32'])

    i += 1

    time.sleep(1.0)
