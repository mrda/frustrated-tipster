#
# predictor.py - base class for prediction engine
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

from abc import ABCMeta, abstractmethod


class Confidence:
    """Simple python2 enum"""
    (StronglyFor, For, Neutral, Against, StronglyAgainst) = (2, 1, 0, -1, -2)


class Predictor:
    """Abstract base class for making footytip predictions"""
    __metaclass__ = ABCMeta

    def __init__(self, name, game_data):
        """Register a name for the predictor and
        provide some data to work with"""
        self.name = name
        self.game_data = game_data

    def get_name(self):
        """Return this predictor's name"""
        return self.name

    @abstractmethod
    def predict(self, game):
        """Make a prediction about a provided game, returning a tuple of the
        team that this predictor thinks is going to win, along with a
        Confidence value about the prediction"""
        pass
