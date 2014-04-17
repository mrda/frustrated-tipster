#!/usr/bin/env python
#
# game_data.py - provide a set of utility functions to find information
#                in historical game data
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


def get_current_year(game_data):
    """Return the current (latest) year"""
    years = sorted(game_data.keys())
    return years[-1]


def get_current_round(game_data, year):
    """Return the current round"""
    rounds = sorted(game_data[year].keys())
    return rounds[-1]


def get_current_year_and_round(game_data):
    """Return the current round and current year"""
    year = get_current_year(game_data)
    rnd = get_current_round(game_data, year)
    return (year, rnd)


def is_minor_round(rnd):
    """Determine whetehr the round specified is a minor round"""
    return rnd.isdigit()


def get_minor_rounds(game_data, year):
    """Return a list of all the minor round for a given year"""
    mrounds = []
    for rnd in game_data[year]:
        if is_minor_round(rnd):
            mrounds.append(rnd)
    return sorted(mrounds, key=int)


def get_team_names(game_data, year):
    """ Return a list of all team names for a given year"""
    # We can't assume that all teams play each week due to split rounds
    # and byes.  Sad.
    teams = []
    for rnd in game_data[year]:
        for game in game_data[year][rnd]:
            game_info = game_data[year][rnd][game]
            if game_info['home_team'] not in teams:
                teams.append(game_info['home_team'])
            if game_info['away_team'] not in teams:
                teams.append(game_info['away_team'])
    return sorted(teams)


def get_games_in_round(game_data, year, rnd):
    return game_data[year][rnd]
