#!/usr/bin/env python
#
# main.py - main entry point for frustrated-tipster
#
import csvparser
import table

#from game import Game
from table_predictor import TablePredictor
from percentage_predictor import PercentagePredictor


# Array of prediction classes to invoke
predictors = []


def register_predictor(predictor_cls):
    predictors.append(predictor_cls)


def predict_result(game):
    print "\nRunning predictions..."
    for predictor in predictors:
        team, confidence = predictor.predict(game)
        print "- Predictor \"%s\" says %s will win, with confidence %s" % (
            predictor.get_name(),
            team,
            confidence)
    print "\n"


def main():
    print "Welcome to frustrated tipster!"
    game_data = csvparser.load_data()

    # Register predictors
    register_predictor(
        TablePredictor("Premiership Table predictor", game_data))
    register_predictor(PercentagePredictor("Percentage predictor", game_data))

    # Print Premiership Table
    print "Print the premiership table for 2013 is"
    t = table.PremiershipTable(game_data)
    tab = t.calculate_table_for_year('2013')
    t.dump_table(tab)

    # Predict a game
    #g = Game('Hawthorn', 'Greater Western Sydney')
    #g = Game('Brisbane Lions', 'North Melbourne')
    #predict_result(g)


if __name__ == '__main__':
    main()
