import threading
import time
import serial
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Frame(object):
    """  Read/Write of serial port, framing and de-framing of data  """

    # some useful constants
    SOF = 0xf7
    EOF = 0x7f
    ESC = 0xf6
    ESC_XOR = 0x20

    def __init__(self, port, timeout=0.1, threaded=True):
        """ Initializes the serial port and creates object threads """
        # initialize the serial port
        try:
            self.port = port
            self.port.flushInput()
            self.raw = []
            self.rx_messages = []

            self.frames = 0
            self.frame_errors = 0

            self.timeout = timeout
            self.threaded = threaded

            if self.threaded:
                thread = threading.Thread(target=self.run, args=())
                thread.daemon = True
                thread.start()

        except serial.SerialException:
            self.port = None
            self.raw = []
            logger.error("Error accessing the serial port")

    def __del__(self):
        """ Closes the serial port """
        if self.port is not None:
            self.port.close()

    @property
    def rx_is_available(self):
        """ Determines if rx data is available and returns the value

        Returns:
            True if de-framed data is available to be read
            False if otherwise
        """
        if len(self.rx_messages) > 0:
            return True
        else:
            return False

    def pull_rx_message(self):
        """ Accesses the rx message and returns it as a list

        Returns:
            the received, de-framed message as a list
        """
        message = []

        if len(self.rx_messages) > 0:
            message = self.rx_messages.pop(0)

        return message

    def push_tx_message(self, message):
        """ Sends a message, performing all framing transparently

        Args:
            message: a list containing the message to be sent
        """
        # start the frame
        frame = [self.SOF]

        # calc the checksum before the framing bits are added
        checksum = self._fletcher16_checksum(message)
        message.append(checksum & 0x00ff)
        message.append((checksum & 0xff00) >> 8)

        for element in message:
            if element == self.SOF or element == self.EOF or element == self.ESC:
                frame.append(self.ESC)
                frame.append(self.ESC_XOR ^ element)
            else:
                frame.append(element)

        frame.append(self.EOF)
        self.port.write(bytearray(frame))

        return

    def _fletcher16_checksum(self, data):
        """ Calculates the fletcher16 checksum on a list of data

        Args:
            data: a list of 8-bit data on which to calculate the checksum

        Returns:
            the fletcher16 checksum
        """
        sum1 = 0
        sum2 = 0

        check_summed_data = data[:]

        for b in check_summed_data:
            sum1 += b
            sum1 &= 0xff  # Results wrapped at 16 bits
            sum2 += sum1
            sum2 &= 0xff

        checksum = (sum2 << 8) | sum1

        return checksum

    def run(self):
        """ Represents the continually executed thread of the object

        This function continually monitors the serial port and de-frames
        the data.  When a complete frame has been received and verified,
        it attaches the de-framed data to the outgoing que to be read.

        """
        run_once = True

        while self.threaded or run_once:
            for element in self.port.read(1000):
                self.raw.append(element)

            # remove leading bytes up to SOF
            while self.raw and self.raw[0] != self.SOF:
                self.raw.pop(0)

            # pull out the frame
            if (self.SOF in self.raw) and (self.EOF in self.raw):
                # find the SOF by removing bytes in front of it
                while self.raw[0] != self.SOF:
                    self.raw.pop(0)

                # find the EOF
                for i, element in enumerate(self.raw):
                    if element == self.EOF:
                        end_char_index = i
                        break
                frame = self.raw[:end_char_index]
                self.raw = self.raw[end_char_index:]

                # remove the SOF and EOF from the frame
                frame.pop(0)

                message = []
                escape_flag = False
                for element in frame:
                    if escape_flag is False:
                        if element == self.ESC:
                            escape_flag = True
                        else:
                            message.append(element)
                    else:
                        message.append(element ^ self.ESC_XOR)
                        escape_flag = False

                # remove the fletcher16 checksum
                f16_check = message.pop(-1) * 256
                f16_check += message.pop(-1)

                self.frames += 1

                # calculate the checksum
                calc_cs = self._fletcher16_checksum(message)
                if calc_cs == f16_check:
                    self.rx_messages.append(message)
                else:
                    self.frame_errors += 1

            run_once = False

            if self.threaded:
                time.sleep(self.timeout)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # define your serial port or supply it otherwise
    port = serial.Serial("COM9", baudrate=57600, timeout=0.1)
    f = Frame(port)

    while True:
        msg = [0, 1, 2, 3, 4, 5, 6, 7]
        f.push_tx_message(msg)
        time.sleep(5.0)

