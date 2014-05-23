#!/usr/bin/env python

"""Command-line interface for boggle solver."""

import argparse
import sys
import os

sys.path.insert(0, os.path.join('..'))

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

    # print("length of args is: " + str(len(args)) + " args are: ")
    # print(args)

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--solve', type=str,
                        help="Add string that represents board. Seperate letters by spaces.")
    parser.add_argument('-p', '--path', type=str,
                        help="Dictionary Path.")

    args = parser.parse_args(args=args)

    if args.path:
        dict_path = os.path.join("docs", args.path)

    if args.solve:
        sb = solve_boggle(args.solve, column, row, dict_path)
        sb.solve()


if __name__ == '__main__':
    main()