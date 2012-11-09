#!/usr/bin/env python

from __future__ import print_function
import argparse
import signal
import sys
import time

import rtmidi


def signal_handler(signal, frame):
    """Handler for Ctrl-C"""
    sys.exit(0)


def midi_in_callback(value, args):
    data = value[0]
    if args['hex']:
        print('[' + ', '.join('0x%02X' % x for x in data) + ']')
    else:
        print(data)


if __name__ == '__main__':
    # Setup command line parser
    parser = argparse.ArgumentParser(description='MIDI tool')
    parser.add_argument('-l', '--list', action='store_true',
                        help='List connected devices')
    parser.add_argument('-d', '--device', metavar='ID',
                        help='Select device')
    parser.add_argument('-w', '--write', type=str, nargs='+', metavar='DATA',
                        help='Write data')
    parser.add_argument('-r', '--read', action='store_true',
                        help='Read data')
    parser.add_argument('-x', '--hex', action='store_true',
                        help='Show/interprete data as hex')
    args = vars(parser.parse_args())

    try:

        if args['list']:
            # List command, show all connected devices
            print()
            print('Available ports:')
            print()
            print('\tInput:')
            print('\t', 'ID', 'Name', sep='\t')
            for i, name in enumerate(rtmidi.MidiIn().get_ports()):
                print('\t', i, name, sep='\t')
            print()
            print('\tOutput:')
            print('\t', 'ID', 'Name', sep='\t')
            for i, name in enumerate(rtmidi.MidiOut().get_ports()):
                print('\t', i, name, sep='\t')
            print()

        elif args['write']:
            # Write command, send data
            if not args['device']:
                raise Exception('No device specified')
            device_id = int(args['device'])
            outport = rtmidi.MidiOut()
            if not device_id < len(outport.get_ports()):
                raise Exception('Device id out of range')
            outport.open_port(device_id)
            if args['hex']:
                data = map(lambda x: int(x, 16), args['write'])
            else:
                data = map(lambda x: int(x, 0), args['write'])
            outport.send_message(data)
            del outport

        elif args['read']:
            # Read command, receive data until Ctrl-C is pressed
            signal.signal(signal.SIGINT, signal_handler)
            if not args['device']:
                raise Exception('No device specified')
            device_id = int(args['device'])
            inport = rtmidi.MidiIn()
            if not device_id < len(inport.get_ports()):
                raise Exception('Device id out of range')
            inport.open_port(device_id)
            inport.set_callback(midi_in_callback, args)
            inport.ignore_types(False, False, False)
            while True:
                time.sleep(1)

    except Exception as e:
        print('Error:', e)
