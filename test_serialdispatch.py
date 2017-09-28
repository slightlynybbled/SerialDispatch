from test_mockserial import MockSerialPort
from serialdispatch.dispatchframe import Frame
from serialdispatch.serialdispatch import SerialDispatch


def test_publish_str():
    """ test publish """
    
    port = MockSerialPort()
    sd = SerialDispatch(port)
    
    # this is the data that should be published
    sd.publish('foo', [['bar']])
    
    # this is the data that should be contained in the serial port outbuffer
    data_test = [Frame.SOF,
                 102, 111, 111, 0,
                 1, 3, 0, 1, 
                 98, 97, 114,
                 126, 22,
                 Frame.EOF]
    
    assert port.serial_data_out == data_test


def test_publish_3_u8():
    port = MockSerialPort()
    sd = SerialDispatch(port)
    
    # this is the data that should be published
    sd.publish('foo', [[10, 20, 30]], ['U8'])
    
    # this is the data that should be contained in the serial port outbuffer
    data_test = [Frame.SOF,
                 102, 111, 111, 0,
                 1, 3, 0, 2, 
                 10, 20, 30,
                 134, 36,
                 Frame.EOF]
    
    assert port.serial_data_out == data_test


def test_publish_3_s8():
    port = MockSerialPort()
    sd = SerialDispatch(port)
    
    # this is the data that should be published
    sd.publish('foo', [[-10, -20, -30]], ['S8'])
    
    # this is the data that should be contained in the serial port outbuffer
    data_test = [Frame.SOF,
                 102, 111, 111, 0,
                 1, 3, 0, 3, 
                 246, 246 ^ 0x20, 236, 226,
                 15, 96,
                 Frame.EOF]
    
    assert port.serial_data_out == data_test


def test_publish_3x3_u8u16u32():
    port = MockSerialPort()
    sd = SerialDispatch(port)
    
    # this is the data that should be published
    sd.publish('foo', [[10, 20, 30], [40, 50, 60], [70, 80, 90]], ['U8', 'U16', 'U32'])
    
    # this is the data that should be contained in the serial port outbuffer
    data_test = [Frame.SOF,
                 102, 111, 111, 0,
                 3, 3, 0, 0x42, 0x06, 
                 10, 20, 30,
                 40, 0, 50, 0, 60, 0,
                 70, 0, 0, 0, 80, 0, 0, 0, 90, 0, 0, 0,
                 84, 186,
                 Frame.EOF]
    
    assert port.serial_data_out == data_test


def test_publish_3x3_s8s16s32():
    port = MockSerialPort()
    sd = SerialDispatch(port)
    
    # this is the data that should be published
    sd.publish('foo', [[-10, -20, -30], [-40, -50, -60], [-70, -80, -90]], ['S8', 'S16', 'S32'])
    
    # this is the data that should be contained in the serial port outbuffer
    data_test = [Frame.SOF,
                 102, 111, 111, 0,
                 3, 3, 0, 0x53, 0x07, 
                 246, 246 ^ 0x20, 236, 226,  # <= one of these happens to be an esc char
                 216, 255, 206, 255, 196, 255,
                 186, 255, 255, 255, 176, 255, 255, 255, 166, 255, 255, 255,
                 214, 236,
                 Frame.EOF]
    
    assert port.serial_data_out == data_test
