from serialdispatch.frame import Frame
from test_mockserial import MockSerialPort
import time


def test_push_tx_message():
    """ Test to ensure that a straightforward frame may be sent """
    
    port = MockSerialPort()
    frame = Frame(port)

    data_to_send = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    frame.push_tx_message(bytearray(data_to_send))

    data_expected = [frame.SOF, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 55, 220, frame.EOF]

    assert set(data_expected) == set(port.serial_data_out)


def test_push_tx_message_with_escapes():
    """ Test to ensure that a frame with all required escape characters may be sent """

    port = MockSerialPort()
    frame = Frame(port)

    data_to_send = [1, 2, frame.SOF, 4, frame.EOF, 6, frame.ESC, 8, 9, 10]
    frame.push_tx_message(bytearray(data_to_send))

    data_expected = [frame.SOF, 1, 2, frame.ESC, frame.SOF ^ frame.ESC_XOR,
                     4, frame.ESC, frame.EOF ^ frame.ESC_XOR,
                     6, frame.ESC, frame.ESC ^ frame.ESC_XOR,
                     8, 9, 10, 148, 20, frame.EOF]
                     
    assert set(data_expected) == set(port.serial_data_out)


def test_rx_is_available_empty():
    """ At initialization, rx available should be empty """

    port = MockSerialPort()
    frame = Frame(port)

    assert not frame.rx_is_available


def test_rx_is_available():
    """ When *valid* serial data is received, rx available should not be empty """

    port = MockSerialPort()
    frame = Frame(port)

    # this is the serial representation of framed data, with checksum
    port.serial_data_in = [frame.SOF, 1, 2, frame.ESC, frame.SOF ^ frame.ESC_XOR,
                           4, frame.ESC, frame.EOF ^ frame.ESC_XOR,
                           6, frame.ESC, frame.ESC ^ frame.ESC_XOR,
                           8, 9, 10, 148, 20, frame.EOF]
    
    time.sleep(0.1)

    assert frame.rx_is_available is True


def test_pull_rx_message():
    """ Test the retrieval of a message """

    port = MockSerialPort()
    frame = Frame(port)
    
    # this is the serial representation of framed data, with checksum
    port.serial_data_in = [frame.SOF, 1, 2, frame.ESC, frame.SOF ^ frame.ESC_XOR,
                           4, frame.ESC, frame.EOF ^ frame.ESC_XOR,
                           6, frame.ESC, frame.ESC ^ frame.ESC_XOR,
                           8, 9, 10, 148, 20, frame.EOF]
    
    time.sleep(0.1)
    
    # this is the expected 'de-framed' data
    data_to_receive = [1, 2, frame.SOF, 4, frame.EOF, 6, frame.ESC, 8, 9, 10]

    assert frame.pull_rx_message() == data_to_receive


def test_pull_rx_message_corrupted():
    """ Should not receive a corrupted message """
    port = MockSerialPort()
    frame = Frame(port)
    
    # this is the serial representation of framed data, with checksum
    port.serial_data_in = [frame.SOF, 1, 2, frame.ESC, frame.SOF ^ frame.ESC_XOR,
                           4, frame.ESC, frame.EOF ^ frame.ESC_XOR,
                           6, frame.ESC, frame.ESC ^ frame.ESC_XOR,
                           8, 9, 10, 148, 21, frame.EOF]
    
    
    time.sleep(0.1)

    assert frame.pull_rx_message() == []

