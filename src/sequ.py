#!/usr/bin/env python2.7

# Copyright 2013 Kristina Frye
# CS 300
# sequ command, Compliance Level 0
# October 4, 2013
#
# This command takes exactly 2 arguments that must be integers
# and prints out all integers between these numbers (inclusive)
# Success returns a 0
# Failure returns a 1

# argparse allows us to easily parse the input arguments
import argparse

parser = argparse.ArgumentParser(description='The sequ command prints a '
   'sequence of numbers between the "first" and the "last" argument '
   'in increments of 1.') 
parser.add_argument('first', help='The starting integer', type=int)
parser.add_argument('last', help='The ending integer', type=int)

# We use a try/except in order to override the exit status code with 1
# This code is from:
# http://stackoverflow.com/questions/5943249/python-argparse-and-controlling-overriding-the-exit-status-code

try:
   args = parser.parse_args()
except SystemExit:
   exit(1)

# The first argument is not allowed to be bigger than the second 
if(args.first > args.last):
   exit(0)

if(args.last - args.first > 100000000):
   print "The range between first and last must be less than 100000000."
   exit(1)

# Print the sequential numbers
for i in range(args.first, args.last + 1):
   print i

# Success!
exit(0)
