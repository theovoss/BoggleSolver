#!/usr/bin/env python

"""Command-line interface for boggle solver."""

import argparse
import time

from bogglesolver.solve_boggle import SolveBoggle
from bogglesolver.load_english_dictionary import Edict


def main(args=None):
    """
    Main entry point for the Command-line-interface.

    Looking at this for good idea of command line interface.
    http://manpages.ubuntu.com/manpages/trusty/man6/boggle.6.html
    """
    min_length = 3
    column = 4
    row = 4
    game_time = 180

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--play', action='store_true',
                        help="True if you want to play boggle.")
    parser.add_argument('-t', '--time', type=int,
                        help="int game time in seconds.")
    parser.add_argument('-l', '--length', type=int,
                        help="Change the minimum word length.")
    parser.add_argument('-w', '--words', type=str,
                        help="Get all words for a given list of letters.")
    parser.add_argument('-c', '--columns', type=int,
                        help="Set the number of columns.")
    parser.add_argument('-r', '--rows', type=int,
                        help="Set the number of rows.")

    args = parser.parse_args(args=args)

    if args.columns:
        column = args.columns

    if args.rows:
        row = args.rows

    if args.words:
        solver = SolveBoggle(args.words, column, row)
        print(solver.solve(False))

    if args.time:
        game_time = args.time

    if args.length:
        min_length = args.length

    if args.play:
        solver = SolveBoggle()
        solver.set_board(column, row)
        cli_dict = Edict()  # !!! kludge ?
        cli_dict.read_dictionary()  # !!! kludge ?
        words = solver.solve(cli_dict)
        print(solver.boggle)
        print("Play Boggle!!")
        time.sleep(game_time)
        # cont = input('Press enter to see the solution.')
        i = 0
        for i, word in enumerate(words):
            if len(word) >= min_length:
                print(word)
        print(str(i) + " words found.")
        exit()


if __name__ == '__main__':
    main()
