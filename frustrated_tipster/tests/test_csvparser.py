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

"""Test class for parser"""

import unittest

from frustrated_tipster import csvparser


class TestParser(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()
