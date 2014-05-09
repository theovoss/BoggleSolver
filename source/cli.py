#!/usr/bin/env python

"""Command-line interface for boggle solver."""

import os
import sys
import ast
import argparse
import logging

import boggle_board
import load_english_dictionary
import solve_boggle

def main(args=None):
	argparse.ArgumenParser()