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

"""Test class for csvparser"""

import unittest

from frustrated_tipster import csvparser


class TestCSVParser(unittest.TestCase):

    def simple_parse_date_test(self):
        expected = ("Friday", "22", "March", "8:10 pm")
        self.assertEqual(expected,
                         csvparser.parse_date("Friday, 22 March (8:10 pm) "))

    def parse_date_no_time_test(self):
        expected = ("Thursday", "26", "March", None)
        self.assertEqual(expected,
                         csvparser.parse_date("Thursday, 26 March "))

    def parse_date_no_day_test(self):
        expected = ('', "19", "September", "7:30pm")
        self.assertEqual(expected,
                         csvparser.parse_date("19 September (7:30pm) "))

    def parse_filename_for_year_test(self):
        f = ("/home/mrda/src/frustrated-tipster/frustrated_tipster/data/"
             "afl_results_2011.csv")
        game_data = {'2011': csvparser.parse_file(f, '2011')}
        # Games in a regular round
        self.assertEqual(8, len(game_data['2011']['10']))
        # Games in a finals round
        self.assertEqual(4, len(game_data['2011']['FW1']))
        self.assertEqual(2, len(game_data['2011']['FW2']))
        self.assertEqual(2, len(game_data['2011']['FW3']))
        self.assertEqual(1, len(game_data['2011']['GF']))
        # Total Rounds in season
        self.assertEqual(28, len(game_data['2011']))
        # Total Games in season
        games = 0
        for round in game_data['2011']:
            games += len(game_data['2011'][round])
        self.assertEqual(196, games)
        # Years present
        self.assertEqual(1, len(game_data))

    def parse_number_of_games_in_round_test(self):
        game_data = csvparser.load_data()
        # Games in a regular round
        self.assertEqual(9, len(game_data['2012']['10']))
        # Games in a finals round
        self.assertEqual(4, len(game_data['2012']['FW1']))
        self.assertEqual(2, len(game_data['2012']['FW2']))
        self.assertEqual(2, len(game_data['2012']['FW3']))
        self.assertEqual(1, len(game_data['2012']['GF']))
        # Total Rounds in season
        self.assertEqual(27, len(game_data['2012']))
        # Total Games in season
        games = 0
        for round in game_data['2012']:
            games += len(game_data['2012'][round])
        self.assertEqual(207, games)
        # Years present
        self.assertGreaterEqual(5, len(game_data))

if __name__ == '__main__':
    unittest.main()
