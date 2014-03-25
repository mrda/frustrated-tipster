#!/usr/bin/env python
#
# main.py - main entry point for frustrated-tipster
#
import csvparser


def main():
    print "Welcome to frustrated tipster!"
    csvparser.find_and_parse_files()
    csvparser._dump_data()

if __name__ == '__main__':
    main()
