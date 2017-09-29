import pytest

from test_mockserial import MockSerialPort
from serialdispatch.frame import Frame
from serialdispatch.serialdispatch import SerialDispatch


process_data = None


@pytest.fixture()
def sending_fixture():
    port = MockSerialPort()
    sd = SerialDispatch(port)

    yield port, sd


def test_publish_str(sending_fixture):
    """ test publish """
    
    port, sd = sending_fixture
    
    # this is the data that should be published
    sd.publish('foo', 'bar')
    
    # this is the data that should be contained in the serial port outbuffer
    data_test = [Frame.SOF,
                 102, 111, 111, 0,  # 'foo\0'
                 1, 3, 0, 1,        # 1-dimensional data, length=0x0003, datatype=string
                 98, 97, 114,       # 'bar'
                 126, 22,           # fletcher checksum
                 Frame.EOF]
    
    assert port.serial_data_out == data_test


def test_publish_3_u8(sending_fixture):
    port, sd = sending_fixture
    
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


def test_publish_3_s8(sending_fixture):
    port, sd = sending_fixture
    
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


def test_publish_3x3_u8u16u32(sending_fixture):
    port, sd = sending_fixture
    
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


def test_publish_3x3_s8s16s32(sending_fixture):
    port, sd = sending_fixture
    
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


@pytest.fixture()
def subscribing_fixture():
    global process_data

    port = MockSerialPort()
    sd = SerialDispatch(port, threaded=False)

    process_data = None

    def toggle_flag():
        global process_data
        nonlocal sd
        process_data = sd.get('foo')

    sd.subscribe('foo', toggle_flag)

    yield port, sd


def test_subscribing_init(subscribing_fixture):
    port, sd = subscribing_fixture

    assert process_data is None


def test_subscribing_string(subscribing_fixture):
    assert process_data is None

    port, sd = subscribing_fixture

    port.serial_data_in = [
        Frame.SOF,
        102, 111, 111, 0,  # 'foo\0'
        1, 3, 0, 1,        # 1-dimensional data, length=0x0003, datatype=string
        98, 97, 114,       # 'bar'
        126, 22,           # fletcher checksum
        Frame.EOF
    ]

    sd.run()

    assert process_data
    assert process_data == 'bar'


def test_subscribing_3_u8(subscribing_fixture):
    assert process_data is None

    port, sd = subscribing_fixture

    port.serial_data_in = [
        Frame.SOF,
        102, 111, 111, 0,
        1, 3, 0, 2,
        10, 20, 30,
        134, 36,
        Frame.EOF
    ]

    sd.run()

    assert process_data
    assert process_data[0] == [10, 20, 30]


def test_subscribing_3_s8(subscribing_fixture):
    assert process_data is None

    port, sd = subscribing_fixture

    # this is the data that should be contained in the serial port input buffer
    port.serial_data_in = [
        Frame.SOF,
        102, 111, 111, 0,
        1, 3, 0, 3,
        246, 246 ^ 0x20, 236, 226,
        15, 96,
        Frame.EOF
    ]

    sd.run()

    assert process_data
    assert process_data[0] == [-10, -20, -30]


def test_subscribing_3x3_u8u16u32(subscribing_fixture):
    assert process_data is None

    port, sd = subscribing_fixture

    # this is the data that should be contained in the serial port input buffer
    port.serial_data_in = [
        Frame.SOF,
        102, 111, 111, 0,
        3, 3, 0, 0x42, 0x06,
        10, 20, 30,
        40, 0, 50, 0, 60, 0,
        70, 0, 0, 0, 80, 0, 0, 0, 90, 0, 0, 0,
        84, 186,
        Frame.EOF
    ]

    sd.run()

    assert process_data
    assert process_data[0] == [10, 20, 30]
    assert process_data[1] == [40, 50, 60]
    assert process_data[2] == [70, 80, 90]


def test_subscribe_3x3_s8s16s32(subscribing_fixture):
    assert process_data is None

    port, sd = subscribing_fixture

    # this is the data that should be contained in the serial port input buffer
    port.serial_data_in = [
        Frame.SOF,
        102, 111, 111, 0,
        3, 3, 0, 0x53, 0x07,
        246, 246 ^ 0x20, 236, 226,  # <= one of these happens to be an esc char
        216, 255, 206, 255, 196, 255,
        186, 255, 255, 255, 176, 255, 255, 255, 166, 255, 255, 255,
        214, 236,
        Frame.EOF
    ]

    sd.run()

    assert process_data
    assert process_data[0] == [-10, -20, -30]
    assert process_data[1] == [-40, -50, -60]
    assert process_data[2] == [-70, -80, -90]
