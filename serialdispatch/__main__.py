import logging
import time
from datetime import datetime

import click
from serial import Serial

from serialdispatch import __version__
from serialdispatch import SerialDispatch
from serialdispatch.sdisplot import PlotApp


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

    plot_app, log_display, csv_file = None, None, None

    def plot(data):
        """ this will plot the received data """

        logger.debug('plot data received: {}'.format(data))

        nonlocal plot_app
        if not plot_app:
            plot_app = PlotApp()

        plot_app.load_new_data(data)

    def log(data):
        if not log_path:
            raise ValueError('log path must be supplied')

        with open(log_path, 'a') as f:
            f.write('{} - {}\n'.format(datetime.now(), data))

    def csv(data):
        raise NotImplementedError

    sd.subscribe('plot', plot)
    sd.subscribe('log', log)
    sd.subscribe('csv', csv)

    while True:
        time.sleep(0)

if __name__ == '__main__':
    main()
