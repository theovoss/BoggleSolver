#!/usr/bin/env python

"""Command-line interface for boggle solver."""

import argparse

# from bogglesolver.boggle_board import boggle
# from bogglesolver.load_english_dictionary import e_dict


def main(args=None):
    """
    Main entry point for the Command-line-interface.

    Currently not implemented.
    """
    print(args)
    parser = argparse.ArgumentParser()
    parser.add_argument('-F', '--no-reformat', action='store_true',
                        help="do not reformat item files during validation")

if __name__ == '__main__':
    main()