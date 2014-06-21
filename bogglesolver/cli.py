#!/usr/bin/env python

"""Command-line interface for boggle solver."""

import argparse
import sys
import os
import time


from bogglesolver.boggle_board import boggle
from bogglesolver.load_english_dictionary import e_dict
from bogglesolver.solve_boggle import solve_boggle


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
    parser.add_argument('-b', '--board', type=str,
                        help="String representing the Boggle Board. Prints out boards solutions. Currently not implemented.")
    parser.add_argument('-t', '--time', type=int,
                        help="int game time in seconds.")
    parser.add_argument('-l', '--length', type=int,
                        help="Change the minimum word length.")
    parser.add_argument('-w', '--words', type=str,
                        help="Get all words for a given list of letters.")

    args = parser.parse_args(args=args)

    if args.words:
        sb = solve_boggle(args.words)
        print(sb.solve(False))

    if args.time:
        game_time = args.time

    if args.length:
        min_length = args.length

    if args.play:
        sb = solve_boggle(['a'] * 16, column, row)
        sb.boggle.generate_boggle_board()
        words = sb.solve()
        print(sb.boggle)
        print("Play Boggle!!")
        time.sleep(game_time)
        # cont = input('Press enter to see the solution.')
        i = 0
        for word in words:
            if len(word) >= min_length:
                print(word)
                i += 1
        print(str(i) + " words found.")
        exit()


if __name__ == '__main__':
    main()
