#
# percentage_predictor.py - make a prediction based upon percentage
#                           as reported by the premiership table
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

from predictor import Predictor, Confidence
from table import PremiershipTable


class PercentagePredictor(Predictor):

    def predict(self, game):
        table = PremiershipTable(self.game_data)
        ptable = table.calculate_current_table()
        home_pos = 0
        away_pos = 0

        # Iterate over the premierships table
        for idx, row in enumerate(ptable):
            if row['team'] == game.home_team:
                home_pos = idx
                home_points = row['points']
                home_percent = row['percentage']
            if row['team'] == game.away_team:
                away_pos = idx
                away_points = row['points']
                away_percent = row['percentage']

        # Make predictions based on points and percentage
        team = None
        confidence = Confidence.For

        if home_points > away_points:
            # home team favoured
            team = ptable[home_pos]['team']
            # If they are very far apart, be more confident
            if home_percent > (away_percent * 1.5):
                confidence = Confidence.StronglyFor
        elif away_points > home_points:
            # away team favoured
            team = ptable[away_pos]['team']
            # If they are very far apart, be more confident
            if away_percent > (home_percent * 1.5):
                confidence = Confidence.StronglyFor
        else:
            # Same points
            if home_percent > away_percent:
                team = ptable[home_pos]['team']
            else:
                team = ptable[away_pos]['team']

        return (team, confidence)
