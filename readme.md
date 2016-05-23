# Purpose #

Sister library to the [Dispatch](https://github.com/slightlynybbled/Dispatch) project.

# Project Maturity #

The project has been informally tested but has very little test coverage at this point.
Tests are separated into their own files and can be executed individually using pytest.
Tests files are prefixed with `test_`.  Tests can be executed using pytest:

    py.test test_frame.py
    
# Quick Usage Notes #

## Setup ##

    pip install serialdispatch

## Initialization ##

The `SerialDispatch` object must be created before accessing any of the SerialDispatch methods.
On instantiation, `SerialDispatch` must be supplied with a port which is byte-aligned and
has the same methods available as the Python `serial` library.  It is assumed that this
will be a serial port; however, there is nothing that would stop it from being any other
byte-aligned communications channel that has the same interface.

    port = serial.Serial("COM9", baudrate=57600, timeout=0.1)
    ps = serialdispatch.SerialDispatch(port)

## Subscribing ##

Subscribing is done using the `SerialDispatch.subscribe()` function.  This function takes
two parameters, the topic and the function to associate with the topic.  Continuing
with the starting code above:

    def my_subscriber_function():
        print('subscriber executed')
        
    ps.subscribe('foo', my_subscriber_function)
    #                           ^ subscribing function
    #              ^ topic
    
After executing the above code, every time that the topic `foo` is received, the string
'subscriber executed' will be output to the console.

## Retrieving Data ##

When data is received on a topic, it is stored by topic.  Usually, the data will be
retrieved by the subscriber, but doesn't have to be.

    data = ps.get_data('foo')
    #                    ^ topic to get data from
    
The format of datais in the form of a list of lists.  A list of lists allows us to receive
multi-dimensional data within a single message.  For instance, if data to be sent was a series
of (x, y) coordinates, we get all of the data at once:

    xy_data = ps.get_data('xy') # assuming topic is called 'xy'
    x = xy_data[0]
    y = xy_data[1]
    # now do some stuff with the data...

## Publishing ##

Publishing to a topic is simple, but has to follow a format as well.  If you simply want to
send a string, you can simply

    ps.publish('foo', [['my string']])
    #                        ^ string within a list of lists
    #            ^ topic
    
This will publish 'my string' to the topic 'foo'.  Again, note that this is a list of lists.  This
format allows us - again - to publish multi-dimensional data.  If the data is any format but a string,
it must have another list with all format specifiers that correspond to the data formats.

Using the (x, y) idea once again, the data is in two dimensions.

    x = [... some unsigned 8-bit numbers ...]
    y = [... some signed 16-bit numbers ...]
    ps.publish('xy', [x, y], ['U8', 'S16'])
    #                              ^ list of format specifiers
    #                  ^ data
    #            ^ topic
    
Strings can only be 1 dimensional.  The length of x and y must be the same.  The currently-supported
format specifiers:

 * STRING
 * U8
 * S8
 * U16
 * S16
 * U32
 * S32
 
# More details #

You can find more details at [for(embed)](http://www.forembed.com/category/dispatch.html).

# Example Usage #

    import serialdispatch

    # define your serial port or supply it otherwise
    port = serial.Serial("COM9", baudrate=57600, timeout=0.1)

    # create a new instance of SerialDispatch
    ps = serialdispatch.SerialDispatch(port)

    # create your subscribers
    def array_subscriber():
        # retrieve received data for topic 'bar' and print to screen
        print('data: ', ps.get_data('bar'))

    def i_subscriber():
        # retrieve received data for topic 'i' and print to screen
        print('i: ', ps.get_data('i'))

    # use the instance of SerialDispatch to associate the subscriber function with the topic
    ps.subscribe('bar', array_subscriber)
    ps.subscribe('i', i_subscriber)

    # publish to topics as desired
    while True:
        ''' publish 'a test message', to subscribers of 'foo', note
            that the message must be in a list of lists '''
        ps.publish('foo', [['a test message']])
        time.sleep(0.4)

# Contributions #

To make a contribution, simply fork the repository. Create a branch that is appropriately descriptive
of your change and perform your development. When complete, create a pull request using that
branch - DO NOT merge into master! Once the proper test coverage is added and passing on TravisCI,
then we can merge into the master branch.

In some cases in which the documentation or examples are contributed, this process will be fast-tracked.
