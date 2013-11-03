#!/usr/bin/env python2.7

# Copyright 2013 Kristina Frye
# CS 300
# sequ command, Compliance Level 1
# November 2, 2013 
#

# argparse allows us to easily parse the input arguments
import argparse

parser = argparse.ArgumentParser(description='The sequ command prints a '
   'sequence of numbers between the "first" and the "last" argument '
   'in increments of 1.')
parser.add_argument('first', help='The starting integer', type=float, nargs='?',
   default=1)
parser.add_argument('increment', help='The increment between numbers',
   type=float, nargs='?', default=1)
parser.add_argument('last', help='The ending integer', type=float)
parser.add_argument('-f', '--format', help='Special formatting', nargs='?')

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

# Limit the range so my computer doesn't run out of memory
if(args.last - args.first > 100000000):
   print "The range between first and last must be less than 100000000."
   exit(1)

# Print the sequential numbers
i = args.first
while(i <= args.last):
   if args.format == None:
      print "%g" % i
   else:
      print args.format % i 
   i = i + args.increment
 
# Success!
exit(0)
