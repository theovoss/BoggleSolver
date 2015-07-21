#!/usr/bin/env python
# pylint: disable=R0912
"""Adjacency functions used to solve the board.

In a separate file for easier modification, and to better show multiple possibilities.
WARNING: the adjacency function will be called a lot. optimize it for speed if you modify
    or create your own.
The examples are optimized for speed.
If you find faster ways to do this please share.
If you have speed issues using your own function, optimize it for speed.
"""


def get_standard_boggle_adjacent(index, num_columns, num_rows, ignore=None):
    """
    Get all adjacent indexes for a standard boggle board.

    Ignore is meant to be the disabled or previously traversed indexes.

    :param int index: index to get all adjacent indexes of.
    :param int num_columns: number of columns in the board.
    :param int num_rows: number of rows in the board.
    :param list ignore: optional list of indexes to ignore.
    :yields: the adjacent indices.
    """
    if ignore is None:
        ignore = []

    row = index // num_columns
    column = index % num_columns

    # calculate the 8 indexes that surround this index

    # index directly to the left:
    if column != 0:
        one_less = index - 1
        if one_less not in ignore:
            yield one_less
        # diagonal up and left
        if row != 0 and one_less - num_columns not in ignore:
            yield one_less - num_columns
        # diagonal down and left
        if row != num_rows - 1 and one_less + num_columns not in ignore:
            yield one_less + num_columns

    # index directly to the right:
    if column != num_columns - 1:
        one_more = index + 1
        if one_more not in ignore:
            yield one_more
        # index to the top right
        if row != 0 and one_more - num_columns not in ignore:
            yield one_more - num_columns
        # index to the bottom right
        if row != num_rows - 1 and one_more + num_columns not in ignore:
            yield one_more + num_columns

    # directly above
    if row != 0 and index - num_columns not in ignore:
        yield index - num_columns

    # directly below
    if row != num_rows - 1 and index + num_columns not in ignore:
        yield index + num_columns


def get_toroid_boggle_adjacent(index, num_columns, num_rows, ignore=None):
    """
    Get all adjacent indexes where the left edge is next to the right edge and the top is next to the bottom.

    Ignore is meant to be the disabled or previously traversed indexes.

    :param int index: index to get all adjacent indexes of.
    :param int num_columns: number of columns in the board.
    :param int num_rows: number of rows in the board.
    :param list ignore: optional list of indexes to ignore.
    :yields: the adjacent indices.
    """
    if ignore is None:
        ignore = []

    row = index // num_columns
    column = index % num_columns

    # calculate the 8 indexes that surround this index

    # index directly to the left:
    one_less = index - 1
    if column == 0:
        one_less = one_less + num_columns

    if one_less not in ignore:
        yield one_less
    # diagonal up and left
    if row != 0:
        if one_less - num_columns not in ignore:
            yield one_less - num_columns
    else:
        if one_less + (num_columns * (num_rows - 1)) not in ignore:
            yield one_less + (num_columns * (num_rows - 1))
    # diagonal down and left
    if row != num_rows - 1:
        if one_less + num_columns not in ignore:
            yield one_less + num_columns
    else:
        if one_less % num_columns not in ignore:
            yield one_less % num_columns

    # index directly to the right:
    one_more = index + 1
    if column == num_columns - 1:
        one_more = one_more - num_columns
    if one_more not in ignore:
        yield one_more

    if row != 0:
        # index to the top right
        if one_more - num_columns not in ignore:
            yield one_more - num_columns
        # directly above
        if index - num_columns not in ignore:
            yield index - num_columns
    else:
        add_to_get_bottom_row = (num_columns * (num_rows - 1))
        # index to the top right
        if one_more + add_to_get_bottom_row not in ignore:
            yield one_more + add_to_get_bottom_row
        # index directly above
        if index + add_to_get_bottom_row not in ignore:
            yield index + add_to_get_bottom_row

    if row != num_rows - 1:
        # index to the bottom right
        if one_more + num_columns not in ignore:
            yield one_more + num_columns
        # directly below
        if index + num_columns not in ignore:
            yield index + num_columns
    else:
        # index to the bottom right
        if one_more % num_columns not in ignore:
            yield one_more % num_columns
        # directly below
        if index % num_columns not in ignore:
            yield index % num_columns


def get_scrabble_adjacent(index, num_columns, num_rows, ignore=None):
    """
    Get all adjacent indexes for solving scrabble.

    WARNING: this does not scale to larger boards as well as the other two
        as it has to return a lot more indeces.

    Basically if it's not the index, and not ignored, yield it.

    Ignore is meant to be the disabled or previously traversed indexes.

    :param int index: index to get all adjacent indexes of.
    :param int num_columns: number of columns in the board.
    :param int num_rows: number of rows in the board.
    :param list ignore: optional list of indexes to ignore.
    :yields: the adjacent indices.
    """
    for i in range(0, num_rows * num_columns):
        if i not in ignore and i is not index:
            yield i
