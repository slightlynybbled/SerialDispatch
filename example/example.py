import serial
import serialdispatch

# the timeout keeps the serial port polling appropriately
port = serial.Serial('COM9', 57600, timeout=0.1)

# a serial port must be supplied to SerialDispatch
sd = serialdispatch.SerialDispatch(port)

def subscriber():
    # the data is retrieved by topic
    data = sd.get_data('subscriber topic')
    print('message received: ', data)
    
sd.subscribe('subscriber topic', subscriber)

while True:
    pass