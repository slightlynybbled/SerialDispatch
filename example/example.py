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


def subscriber():
    # the data is retrieved by topic
    data = sd.get('i')
    print('message received: ', data)
    
sd.subscribe('i', subscriber)

while True:
    sd.publish('foo', [0], ['U16'])
    time.sleep(1.0)
