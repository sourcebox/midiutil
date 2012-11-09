# midiutil

## Synopsis

midiutil is a command line tool written in Python for debugging and testing MIDI devices.
It can send specific data to MIDI devices known by the host, either virtual, via USB directly or a dedicated MIDI interface. It also allows
to monitor incoming data.

## Requirements

- Python 2.7
- [python-rtmidi](http://pypi.python.org/pypi/python-rtmidi/)

midiutil was developed and tested under OS X.

## Quick Start

	$ ./midiutil.py -h

Shows available options.

	$ ./midiutil.py -l

Lists available MIDI devices, seperated by inputs and outputs.
Each device has an ID which has to be used to select the device
when transmitting data.

### Sending MIDI data

	$ ./midiutil.py -d ID -w DATA [DATA ...]

Sends data to a device.

Example:

	$ ./midiutil.py -d 2 -w 0x90 60 127

In the example above, a Note On message on MIDI channel 1 with note number 60 and a velocity of 127 is sent to output device id 2.
Numbers prefixed with 0x are interpreted as hex values.

### Monitoring MIDI data

	$ ./midiutil.py -d ID -r [-x]

Listens to data from a device and displays it.

Example:

	$ ./midiutil.py -d 2 -r

Shows incoming messages from input device id 2.

To display data as hex values, add the `-x` switch to the command:

	$ ./midiutil.py -d 2 -x

Use `Ctrl-C` to abort monitoring and return to the command prompt.

## License

This tool is released under the BSD license.

## Todo

- Python 3 support
- Testing on MS Windows platforms
- Support for device names instead of numeric IDs
- More options :-)
