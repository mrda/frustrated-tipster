#!/usr/bin/env python
#
# csvparser.py - Read the AFL results files, and build up a dictionary
#                of what we find
#
# Turn on debugging by 'export TIPPING_DEBUG=1' in your shell
#
# (data obtained from wikipedia -
#  see http://en.wikipedia.org/wiki/20XX_AFL_season)
#
# Copyright (C) 2013, 2014 Michael Davies <michael@the-davies.net>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
# Or try here: http://www.fsf.org/copyleft/gpl.html

import csv
import os
import re


FILENAME_RE = re.compile(r'(.*)(\d{4})\.csv')
DATE_RE = re.compile((r'(?P<day>[a-zA-z]*)(\,\s)?(?P<date>\d{1,2}) '
                      '(?P<month>[a-zA-Z]+)\s(\((?P<time>\d\:\d{1,2}(\s)?'
                      '(a|p)m)\))?'))
TEAM_RE = re.compile((r'(?P<name>.*)\s+((?P<goals>\d+)\.(?P<points>\d+)(\.)?\s?'
                      '\((?P<total>\d+)\))?'))
GROUND_RE = re.compile((r'(?P<name>.*)\s\((C|c)rowd\:\s+'
                        '(?P<attendance>\d+,?\d+)?'))


debug = False
interactive = False


def parse_date(string):
    # return the day, date and time as a dict
    # NOTE(mrda): day and time aren't always there
    m = DATE_RE.match(string)
    if m:
        return (m.group('day'), m.group('date'),
                m.group('month'), m.group('time'))
    else:
        print "*** Couldn't parse date \"" + string + "\""
        return None


def parse_team(string):
    # return the team name, the goals, the points,
    # and the total score as a dict
    m = TEAM_RE.match(string)
    if m:
        return (m.group('name'), m.group('goals'),
                m.group('points'), m.group('total'))
    else:
        print "*** Couldn't parse team \"" + string + "\""
        return None


def parse_result(str):
    # return "won", "loss", or "draw" as a string
    if str.strip() == 'def. by':
        return 'lost to'
    elif str.strip() == 'def.':
        return 'defeated'
    elif str.strip() == 'drew with':
        return 'drew'
    elif str.strip() == 'vs.':
        return 'verses'
    else:
        print "*** Couldn't parse result \"" + str + "\""
        return None


def parse_ground(string):
    # return the ground name and the crowd as a dict
    m = GROUND_RE.match(string)
    if m:
        return (m.group('name'), m.group('attendance'))
    else:
        print "*** Couldn't parse ground \"" + string + "\""
        return None


def parse_year(filename):
    # Decode and return the start of the string, and the year
    # embedded in a filename.  Format is somestring_year.csv
    m = FILENAME_RE.match(filename)
    return (m.group(1), m.group(2))


def _format_day(data, year, round, game):
    if data[year][round][game]['day'] is None:
        return "<Unknown day>"
    else:
        return data[year][round][game]['day']


def _format_time(data, year, round, game):
    if data[year][round][game]['time'] is None:
        return "<Unknown time>"
    else:
        return data[year][round][game]['time']


def _format_date_string(data, year, round, game):
    return (_format_day(data, year, round, game) + " "
            + data[year][round][game]['date'] + " "
            + data[year][round][game]['month'] + " "
            + year + " " + _format_time(data, year, round, game))


def _format_score(data, year, round, game):
    return (data[year][round][game]['home_goals'] + ":" +
            data[year][round][game]['home_points'] + " (" +
            data[year][round][game]['home_total'] + ") to " +
            data[year][round][game]['away_goals'] + "." +
            data[year][round][game]['away_points'] + " (" +
            data[year][round][game]['away_total'] + ")")


def _dump_data(data):
    """ Decode and print all data read from alf_results files """
    for year in sorted(data.keys()):
        print "Year " + year
        for round in sorted(data[year].keys()):
            print "  Round " + str(round)
            for game in sorted(data[year][round].keys()):
                print "    Game " + str(game)
                print "      " + _format_date_string(data, year, round, game)
                print "      " + (data[year][round][game]['home_team'] + " " +
                                  data[year][round][game]['result'] + " " +
                                  data[year][round][game]['away_team'])
                print "      " + _format_score(data, year, round, game)
                print "      " + data[year][round][game]['ground']
                print "      " + data[year][round][game]['attendance']


def _print_row(row):
    """ Decode and print out a row read from an afl_results
        csv file """
    print "Round: \"" + row[0] + "\""
    print "Date: \"" + row[1] + "\""
    print "Home: \"" + row[2] + "\""
    print "Result: \"" + row[3] + "\""
    print "Away: \"" + row[4] + "\""
    print "Ground: \"" + row[5] + "\""
    print "--"


def parse_file(filename, year, debug=False, interactive=False):
    with open(filename) as csvfile:
        data = {}
        last_round = 0
        game = 0
        reader = csv.reader(csvfile, quotechar='"')
        for row in reader:
            if row[0] is "":
                continue
            if interactive:
                _print_row(row)
            round = str(row[0])
            date_tuple = parse_date(row[1])
            home_tuple = parse_team(row[2])
            result = parse_result(row[3])
            away_tuple = parse_team(row[4])
            ground_tuple = parse_ground(row[5])
            # Handle the next round
            if round not in data.keys():
                data[round] = {}
            # Handle game ids
            if round != last_round:
                last_round = round
                game = 1
            else:
                game = game + 1
            data[round][game] = {
                'date': date_tuple[1],
                'month': date_tuple[2],
                'year': year,
                'home_team': home_tuple[0],
                'home_goals': home_tuple[1],
                'home_points': home_tuple[2],
                'home_total': home_tuple[3],
                'result': result,
                'away_team': away_tuple[0],
                'away_goals': away_tuple[1],
                'away_points': away_tuple[2],
                'away_total': away_tuple[3],
                'ground': ground_tuple[0],
                'attendance': ground_tuple[1],
            }
            # Sometimes the day is optional
            if date_tuple[0]:
                data[round][game]['day'] = date_tuple[0]
            else:
                data[round][game]['day'] = None
            # Sometimes the time is optional
            if date_tuple[3]:
                data[round][game]['time'] = date_tuple[3]
            else:
                data[round][game]['time'] = None
        return data


def find_and_parse_files(debug, interactive):
    data = {}
    # TODO(mrda): FIXME path
    directory = "/home/mrda/src/frustrated-tipster/frustrated_tipster/data/"
    for fn in os.listdir(directory):
        filename = directory + fn
        (startstr, year) = parse_year(fn)
        if startstr == 'afl_results_':
            if debug:
                print "--- Parsing " + filename
            data[year] = parse_file(filename, year, debug, interactive)
        else:
            if debug:
                print "%%% Skipping " + filename
    return data


def load_data(debug=False, interactive=False):
    """Load data from disk, and return a dictionary of game data"""
    data = find_and_parse_files(debug, interactive)
    return data


if __name__ == '__main__':
    interactive = True
    if 'TIPPING_DEBUG' in os.environ:
        debug = True
    data = load_data(debug, interactive)
    if interactive:
        _dump_data(data)
