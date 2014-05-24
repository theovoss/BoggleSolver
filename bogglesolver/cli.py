#!/usr/bin/env python

"""Command-line interface for boggle solver."""

import argparse
import sys
import os


from bogglesolver.boggle_board import boggle
from bogglesolver.load_english_dictionary import e_dict
from bogglesolver.solve_boggle import solve_boggle


def main(args=None):
    """
    Main entry point for the Command-line-interface.

    Currently not implemented.
    """
    dict_path = os.path.join("docs", "twl06.txt")
    column = 4
    row = 4

    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--play', action='store_true',
                        help="True if you want to play boggle.")
    parser.add_argument('-b', '--board', type=str,
                        help="String representing the Boggle Board. Prints out boards solutions. Currently not implemented.")

    args = parser.parse_args(args=args)

    if args.play:
        sb = solve_boggle(['a'] * 16, column, row, dict_path)
        sb.boggle.generate_boggle_board()
        words = sb.solve()
        print(sb.boggle)
        cont = raw_input('Press any button to see the solution.')
        for word in words:
            print(word)


if __name__ == '__main__':
    main()