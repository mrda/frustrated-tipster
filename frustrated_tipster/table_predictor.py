#
# table_predictor.py - make a prediction based upon premiership table
#                      position
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


class TablePredictor(Predictor):

    def predict(self, game):
        table = PremiershipTable(self.game_data)
        ptable = table.calculate_current_table()
        home_pos = 0
        away_pos = 0
        confidence = Confidence.For
        # Find the relative positions on the premiership table
        for idx, row in enumerate(ptable):
            if row['team'] == game.home_team:
                home_pos = idx
            if row['team'] == game.away_team:
                away_pos = idx
        # If they are very far apart, be more confident
        if abs(home_pos - away_pos) > (len(ptable) / 2):
            confidence = Confidence.StronglyFor
        # Predict the higher-placed team
        if home_pos > away_pos:
            return (game.away_team, confidence)
        else:
            return (game.home_team, confidence)
