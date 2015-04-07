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

"""Test class for game_data """

import unittest

from frustrated_tipster import game_data as gd
from frustrated_tipster import csvparser


class TestGameData(unittest.TestCase):

    # TODO(mrda): setup test data, don't use real data for current
    def get_current_year_test(self):
        gdata = csvparser.load_data()
        year = gd.get_current_year(gdata)
        self.assertEqual('2014', year)

    # TODO(mrda): setup test data, don't use real data for current
    def get_current_year_and_round_test(self):
        gdata = csvparser.load_data()
        year, rnd = gd.get_current_year_and_round(gdata)
        self.assertEqual(('2014', 'GF'), (year, rnd))

    # TODO(mrda): setup test data, don't use real data for current
    def get_team_names_test(self):
        gdata = csvparser.load_data()
        teams = gd.get_team_names(gdata, '2014')
        print (str(teams))

# TODO(mrda): many more tests needed here
