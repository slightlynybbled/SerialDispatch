class MockSerialPort:
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