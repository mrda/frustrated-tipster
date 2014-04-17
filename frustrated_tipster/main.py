#!/usr/bin/env python
#
# main.py - main entry point for frustrated-tipster
#
import csvparser
import table


def main():
    print "Welcome to frustrated tipster!"
    game_data = csvparser.load_data()

    print "Print the premiership table for 2013 is"
    t = table.PremiershipTable(game_data)
    tab = t.calculate_table_for_year('2013')
    t.dump_table(tab)


if __name__ == '__main__':
    main()
