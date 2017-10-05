import logging
import time
from datetime import datetime

import click
from serial import Serial

from serialdispatch import __version__
from serialdispatch import SerialDispatch


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@click.command()
@click.option('--port', '-p', help='port name')
@click.option('--baudrate', '-b', help='baud rate, bits/s')
@click.option('--log-path', '-l', help='path to log file')
@click.option('--csv-path', '-c', help='path to csv file')
@click.option('--version', '-V', is_flag=True, help='Show software version')
def main(port, baudrate, log_path, csv_path, version):
    if version:
        print('SerialDispatch, v{}'.format(__version__))

    if not port:
        logger.error('port not specified')
        return

    if not baudrate:
        baudrate = 57600
        logger.warning('baudrate not specified, defaulting to {}b/s'.format(baudrate))

    baudrate = int(baudrate)
    logger.info('using {} at {}b/s'.format(port, baudrate))

    port = Serial(port=port, baudrate=baudrate, timeout=0.01)
    sd = SerialDispatch(port=port)

    csv_header = None

    def plot(data):
        nonlocal plot_app
        logger.debug('plot data received: {}'.format(data))

        '''for i, e in enumerate(data):
            add_point(i, e)'''
        raise NotImplementedError

    def log(data):
        if not log_path:
            raise ValueError('log path must be supplied')

        with open(log_path, 'a') as f:
            f.write('{} - {}\n'.format(datetime.now(), data))

    def csv(data):
        nonlocal csv_header

        # a string coming in is most likely a header, parse it and save it
        if isinstance(data, str):
            with open(csv_path, 'a') as f:
                parts = [e.strip() for e in data.split(',')]
                new_header = ','.join(parts)
                if csv_header != new_header:
                    csv_header = new_header
                    f.write(csv_header + '\n')
                return

        if not isinstance(data[0], list):
            with open(csv_path, 'a') as f:
                parts = ['{}'.format(p) for p in data]
                f.write('{}\n'.format(','.join(parts)))

    sd.subscribe('plot', plot)
    sd.subscribe('log', log)
    sd.subscribe('csv', csv)

    while True:
        time.sleep(0)

if __name__ == '__main__':
    main()
