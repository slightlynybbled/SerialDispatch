import logging

import click
from serial import Serial

from serialdispatch import __version__
from serialdispatch import SerialDispatch


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


@click.command()
@click.option('--port', '-p', help='port name')
@click.option('--baudrate', '-b', help='baud rate, bits/s')
@click.option('--version', '-V', is_flag=True, help='Show software version')
def main(port, baudrate, version):
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

    port = Serial(port=port, baudrate=baudrate)
    sd = SerialDispatch(port=port)

    def plot():
        sd.get('show')

    def log():
        sd.get('log')

    def csv():
        sd.get('csv')

    sd.subscribe('show', plot)
    sd.subscribe('log', log)
    sd.subscribe('csv', csv)

if __name__ == '__main__':
    main()
