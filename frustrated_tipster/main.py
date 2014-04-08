#!/usr/bin/env python
#
# main.py - main entry point for frustrated-tipster
#
import csvparser


def main():
    print "Welcome to frustrated tipster!"
    game_data = csvparser.load_data()
    csvparser._dump_data(game_data)

if __name__ == '__main__':
    main()
