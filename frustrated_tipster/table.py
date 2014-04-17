#!/usr/bin/env python
#
# table.py - Generate a premiership table from provided data
#
# Copyright (C) 2014 Michael Davies <michael@the-davies.net>
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

import game_data as gd


class PremiershipTable:
    """Calculate the premiership table"""

    def __init__(self, game_data):
        self.game_data = game_data

    def calculate_table_for_year(self, year):
        rnd = gd.get_current_round(self.game_data, year)
        return self.calculate_table(year, rnd)

    def calculate_table(self, year, rnd):
        minor_rounds = gd.get_minor_rounds(self.game_data, year)
        current_rnd = gd.get_current_round(self.game_data, year)

        # Find the maximum current round that isn't major round
        if not gd.is_minor_round(current_rnd):
            current_rnd = minor_rounds[-1]

        # Setup a blank premiership table first
        ptable = {}
        teams = gd.get_team_names(self.game_data, year)
        for team in teams:
            ptable[team] = {'played': 0,
                            'win': 0,
                            'loss': 0,
                            'draw': 0,
                            'pf': 0,
                            'pa': 0,
                            'percentage': 0.0,
                            'points': 0}

        # Process each round
        for rnd in minor_rounds:
            if int(rnd) > int(current_rnd):
                break
            for game in self.game_data[year][rnd]:
                game_info = self.game_data[year][rnd][game]

                home = game_info['home_team']
                away = game_info['away_team']

                # Update games played
                ptable[home]['played'] += 1
                ptable[away]['played'] += 1

                # Update win/los/draw/points
                if game_info['result'] == 'defeated':
                    ptable[home]['win'] += 1
                    ptable[away]['loss'] += 1
                    ptable[home]['points'] += 4
                elif game_info['result'] == 'lost to':
                    ptable[home]['loss'] += 1
                    ptable[away]['win'] += 1
                    ptable[away]['points'] += 4
                else:  # drew
                    ptable[home]['draw'] += 1
                    ptable[home]['points'] += 2
                    ptable[away]['draw'] += 1
                    ptable[away]['points'] += 2

                # Update PF/PA
                ptable[home]['pf'] += int(game_info['home_total'])
                ptable[home]['pa'] += int(game_info['away_total'])
                ptable[away]['pf'] += int(game_info['away_total'])
                ptable[away]['pa'] += int(game_info['home_total'])

        # Now process percentages.  Only need to do this after we've processed
        # all the rounds that we're going to process
        for team in teams:
            ptable[team]['percentage'] = (
                float(ptable[team]['pf']) /
                float(ptable[team]['pa']) * 100)

        # Convert the dictionary representation to a list representation
        prem_list = []
        for team in teams:
            e = {}
            e['team'] = team
            for f in ptable[team]:
                e[f] = ptable[team][f]
            prem_list.append(e)

        # Sort the premiership table on points, then percentage
        sorted_prem = sorted(prem_list,
            key=lambda e: "%2d %6.2f" % (e['points'], e['percentage']),
            reverse=True)

        return sorted_prem

    def dump_table(self, table):
        print "%-20s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % \
            ("Team",
             "played",
             "won",
             "loss",
             "draw",
             "pf",
             "pa",
             "percent",
             "points")
        #for team in table.keys():
        for row in table:
            print "%-20s\t%s\t%s\t%s\t%s\t%s\t%s\t%6.2f\t%s" % \
                (row['team'],
                 row['played'],
                 row['win'],
                 row['loss'],
                 row['draw'],
                 row['pf'],
                 row['pa'],
                 row['percentage'],
                 row['points'])

    def display_table(self):
        """Calculate the current premiership table and display it"""
        current_year = gd.get_current_year(self.game_data)
        self.display_table_for_year(current_year)

    def display_table_for_year(self, year):
        """Calculate the current premiership table and display it"""
        ptable = self.calculate_table_for_year(year)
        self.dump_table(ptable)


if __name__ == '__main__':
    # Need csvparser for getting the data to read
    import csvparser
    game_data = csvparser.load_data()

    table = PremiershipTable(game_data)

    table.display_table()
