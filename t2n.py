#!/usr/bin/env python2

import argparse
import sys

import nxt.locator
import nxt.error
from nxt.brick import FileFinder, FileReader, FileWriter

def battery(b):
    print '%dmV' % b.get_battery_level()

def informations(b):
    print '#### NXT INFOS ###############'
    ((proto_major, proto_minor), 
     (firm_major, firm_minor)) = b.get_firmware_version()
    print 'protocol version=%d.%d firmware version=%d.%d' % (proto_major, proto_minor, firm_major, firm_minor)
    (name, addr, strength, user_flash) = b.get_device_info()
    print 'NXT Name: %s' % name
    print 'Bluetooth address: %s' % addr
    print 'Bluetooth signal: %d' % strength
    print 'Free user flash: %d' % user_flash

def ls(b):
    f = FileFinder(b, '*')
    for (fname, size) in f:
        print fname

def get(b, fname):
    r = FileReader(b, fname)
    print 'Getting file %s ...' % fname,
    sys.stdout.flush()
    data = r.read()
    print 'retrieved %d bytes' % len(data)

    f = open(fname, 'w')
    f.write(data)
    f.close()
    r.close()

def put(b, fname):
    f = open(fname)
    data = f.read()
    f.close()
    try:
        b.delete(fname)
        print 'Replacing %s on NXT' % fname
    except nxt.error.FileNotFound:
        pass
    
    w = FileWriter(b, fname, len(data))
    print 'Writing %s (%d bytes) ...' % (fname, w.size),
    sys.stdout.flush()
    w.write(data)
    print 'wrote %d bytes' % len(data)
    w.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Talk to NXT with Python')
    parser.add_argument('-b', action='append_const', dest='action', 
                        const=battery, help='Check battery level')
    parser.add_argument('-i', action='append_const', dest='action',
                        const=informations, help='Print NXT info')
    parser.add_argument('-ls', action='append_const', dest='action',
                        const=ls, help='List files')
    parser.add_argument('-put', metavar='<file>', action='append', help='Upload file')
    parser.add_argument('-get', metavar='<file>', action='append', help='Download file')
    parser.add_argument('-version', action='version', version='%(prog)s 0.0')
    if sys.argv[1:] == []:
        parser.print_help()
        exit(0)
    args = parser.parse_args()
    try:
        b = nxt.locator.find_one_brick()
        for action in args.action:
            action(b)
        for f in args.put:
            get(b, f)
        for f in args.get:
            put(b, f)
    except nxt.locator.BrickNotFoundError:
        print 'Can\'t find any NXT brick connected'
    except:
        print 'Unexpected error'
        raise
