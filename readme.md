![Travis CI Build Status - Master Branch](https://travis-ci.org/slightlynybbled/SerialDispatch.svg?branch=master)

# Purpose #

Sister library to the [Dispatch](https://github.com/slightlynybbled/Dispatch) project.

# Project Maturity #

The project has some testing implemented.  Testing is done using the `pytest` framework.
Simply navigate to the root directory and execute

    py.test
    
I have verified that `serialdispatch` works on Python3 in Windows 10, Ubuntu, and on the 
Raspberry Pi 2 (a Debian distribution) within the 
[curve tracer project](http://www.forembed.com/category/curve-tracer.html).
    
# Quick Usage Notes #

## Setup ##

    pip install serialdispatch
    
## Operating Modes ##

There are two ways to utilize `SerialDispatch`, embedded within your application or free-running.  When embedded, `serialdispatch` works as a middle man which can publish and subscribe to data streams.  When free-running, `serialdispatch` subscribes to the `log` and `csv` messages, allowing you to easily archive any information received on the serial port.

## Free-Running ##

Free-running mode is the simplest way to log your microcontroller messages and data with very little effort.

### Initialization ###

Simply `serialdispatch <options>` and the application will wait to write to CSV files or to logs.

    Usage: serialdispatch [OPTIONS]
    
    Options:
      -p, --port TEXT      port name
      -b, --baudrate TEXT  baud rate, bits/s
      -l, --log-path TEXT  path to log file
      -c, --csv-path TEXT  path to csv file
      -V, --version        Show software version
      --help               Show this message and exit.
      
An example might be:

    $ > serialdispatch --port COM4 --log-path log.txt --csv-path dat.csv
    
Now, on your microcontroller, you can simply publish to 'log' and 'csv' in order to archive data!

    /* publish to a log */
    DIS_publish("log", "the event occured!");
    
    /* publish to a csv file using the lettered column headers */
    DIS_publish("csv", "a, b, c, d,e,f,g,h,i,j");
    DIS_publish("csv:10,u8", arrayToPlot);
        
The `log.txt` will be appended with `2017-11-13 11:56:47.612014 - the event occured!` and the `dat.csv` will be appended with the array data.

## Embedded ##

### Initialization ###

The `SerialDispatch` object must be created before accessing any of the SerialDispatch methods.
On instantiation, `SerialDispatch` must be supplied with a port which is byte-aligned and
has the same methods available as the Python `serial` library.  It is assumed that this
will be a serial port; however, there is nothing that would stop it from being any other
byte-aligned communications channel that has the same interface.

    port = serial.Serial("COM9", baudrate=57600, timeout=0.1)
    ps = serialdispatch.SerialDispatch(port)

### Subscribing ###

Subscribing is done using the `SerialDispatch.subscribe()` function.  This function takes
two parameters, the topic and the function to associate with the topic.  Continuing
with the starting code above:

```python
def my_subscriber_function(data):
    print('subscriber executed, received data: ', data)
    
ps.subscribe('foo', my_subscriber_function)
#                           ^ subscribing function
#              ^ topic
```
    
After executing the above code, every time that the topic `foo` is received, the string
`subscriber executed, received data: ` will be output to the console along with the received data.

The format of data depends on the format of the data received.  If the data received is in the format
of a string, then a string is returned.  If the data received is a single numerical value, then the
numerical value is returned.  If the data received is an array of data, then the array is returned in
the form of a Python list, and if multiple arrays are returned, then a list of lists is generated.

A list of lists allows us to receive multi-dimensional data within a single message.  For instance,
if data to be sent was a series of (x, y) coordinates, we get all of the data at once.  Note that this
must be done from within the callback:

```python
def my_callback(data)
    x, y = data  # split the data into the two expected values

    # now do some stuff with the data...
```

### Publishing ###

Publishing to a topic is simple, but has to follow a format as well.  If you simply want to
send a string, you can simply

```python 
ps.publish('foo', 'my string')
#                     ^ string
#            ^ topic
```

This will publish 'my string' to the topic 'foo'.

Using the (x, y) idea once again, the data is in two dimensions.

```python 
x = [... some unsigned 8-bit numbers ...]
y = [... some signed 16-bit numbers ...]
ps.publish('xy', [x, y], ['U8', 'S16'])
#                              ^ list of format specifiers
#                  ^ data
#            ^ topic
```
    
Strings can only be 1 dimensional.  The length of x and y must be the same.  The currently-supported
format specifiers:

 * `STRING`
 * `U8`
 * `S8`
 * `U16`
 * `S16`
 * `U32`
 * `S32`

# More details #

You can find more details at [for(embed)](http://www.forembed.com/category/dispatch.html).

# Example Usage #

There is a working example that demonstrates working with multiple data types within
the `/examples` directory.  A quick - but complete - example is shown below.

```python
import serialdispatch

# define your serial port or supply it otherwise
port = serial.Serial("COM9", baudrate=57600, timeout=0.01)

# create a new instance of SerialDispatch
ps = serialdispatch.SerialDispatch(port)

# create your subscribers
def array_subscriber(data):
    # retrieve received data for topic 'bar' and print to screen
    print('data: ', data)

def i_subscriber(data):
    # retrieve received data for topic 'i' and print to screen
    print('i: ', data)

# use the instance of SerialDispatch to associate the subscriber function with the topic
ps.subscribe('bar', array_subscriber)
ps.subscribe('i', i_subscriber)

# publish to topics as desired
while True:
    ''' publish 'a test message', to subscribers of 'foo', note
        that the message must be in a list of lists '''
    ps.publish('foo', 'a test message')
    time.sleep(1.0)
```

# Contributions #

To make a contribution, simply fork the repository. Create a branch that is appropriately descriptive
of your change and perform your development. When complete, create a pull request using that
branch - DO NOT merge into master! Once the proper test coverage is added and passing on TravisCI,
then we can merge into the master branch.

In some cases in which the documentation or examples are contributed, this process will be fast-tracked.
