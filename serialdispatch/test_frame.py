from frame import Frame
import serial
import pytest
import time


class MockSerialPort(serial.Serial):
    """ This is a class that will provide a mock interface for the serial port """

    def __init__(self):
        self.serial_data_out = []
        self.serial_data_in = []

    def close(self):
        del self.serial_data_out

    def flushInput(self):
        self.serial_data_in = []

    def write(self, byte_array):
        for e in byte_array:
            self.serial_data_out.append(e)

    def read(self, num_of_bytes):
        data_to_return = self.serial_data_in[:num_of_bytes]
        self.serial_data_in = self.serial_data_in[num_of_bytes:]
        return data_to_return


def test_send():
    port = MockSerialPort()
    frame = Frame(port)

    data_to_send = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    frame.push_tx_message(bytearray(data_to_send))

    data_expected = [frame.SOF, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 55, 220, frame.EOF]
    print('expected: ', data_expected)
    print('actual:   ', port.serial_data_out)

    assert set(data_expected) == set(port.serial_data_out)


def test_send_with_escapes():
    port = MockSerialPort()
    frame = Frame(port)

    data_to_send = [1, 2, frame.SOF, 4, frame.EOF, 6, frame.ESC, 8, 9, 10]
    frame.push_tx_message(bytearray(data_to_send))

    data_expected = [frame.SOF, 1, 2, frame.ESC, frame.SOF ^ frame.ESC_XOR,
                     4, frame.ESC, frame.EOF ^ frame.ESC_XOR,
                     6, frame.ESC, frame.ESC ^ frame.ESC_XOR,
                     8, 9, 10, 148, 20, frame.EOF]
    print('expected: ', data_expected)
    print('actual:   ', port.serial_data_out)

    assert set(data_expected) == set(port.serial_data_out)


def test_rx_is_available_empty():
    port = MockSerialPort()
    frame = Frame(port)

    assert not frame.rx_is_available()


def test_rx_is_available():
    port = MockSerialPort()
    frame = Frame(port)

    port.serial_data_in = [1, 2, 3]
    time.sleep(0.1)

    assert frame.rx_is_available() is True


