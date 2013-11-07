#!/usr/bin/env python2.7

# Copyright 2013 Kristina Frye
# CS 300
# sequ command, Compliance Level 1
# November 2, 2013 
#

# argparse allows us to easily parse the input arguments
from __future__ import print_function
import argparse
from decimal import Decimal

# Set up the parser
parser = argparse.ArgumentParser(description='The sequ command prints a '
   'sequence of numbers between the "first" and the "last" argument '
   'in increments of "increment," which defaults to 1.')

# We do not allow multiple simultaneous print options
group = parser.add_mutually_exclusive_group()

# Get first number. This is optional and defaults to 1
parser.add_argument('first', 
   help='The starting integer (default=1)', type=float, nargs='?', default=1)

# Get increment number. This is optional and defaults to 1
parser.add_argument('increment', 
   help='The increment between numbers (default=1)', 
   type=float, nargs='?', default=1)

# Get the last number. This number is required
parser.add_argument('last', help='The ending integer', type=float)

# Get the options. Can only specify 1.
group.add_argument('-f', '--format', dest='string_format', 
   help='Special formatting', nargs='?')
group.add_argument('-w', '--equal-width', dest='equalwidth',
   action='store_true', 
   help='Print all numbers with same width with zero padding, if necessary.')
group.add_argument('-s', '--separator', 
   help='Print with separator instead of each number on own line', nargs='?')

# We use a try/except in order to override the exit status code with 1
# This code is from:
# http://stackoverflow.com/questions/5943249/python-argparse-and-controlling-overriding-the-exit-status-code

try:
   args = parser.parse_args()
except SystemExit:
   exit(1)

# The first argument is not allowed to be bigger than the second 
if(args.first > args.last):
   if(args.increment > 0):
      exit(0)

# Limit the range so my computer doesn't run out of memory
if(abs(args.last - args.first) > 100000000):
   print("The range between first and last must be less than 100000000.")
   exit(1)

# The increment cannot be zero
if(args.increment == 0):
   print("The increment cannot be 0")
   exit(1)

# This function is only used when the option is set to -w (equal-width)
# This function is used to get the maximum character length and the
# decimal precision. Since this might change depending upon whether a decimal 
# point is used and whether the increment is factional, we will iterate 
# through the entire loop to get the maximum length.
# Need to be able to find the number of decimal places of a 
# formatted string:
# http://stackoverflow.com/questions/6189956/easy-way-of-finding-decimal-places

def get_max_length(first, last, increment):
   max_length = 0       #initialize the max lengths
   max_dec_length = 0
   current_num = first  #initialize the current number counter
   run_loop = True

   while(run_loop == True):
      formatted_string = str("{0:g}".format(current_num))

      # Calculate the string lengths and precision
      length = len(formatted_string)
      dec_length = abs(Decimal(formatted_string).as_tuple().exponent)
      
      # Check if greater than max lengths
      if(max_length < length):
         max_length = length
      if(max_dec_length < dec_length):
         max_dec_length = dec_length

      #increment the number
      current_num = current_num + increment
      
      #check if the loop should continue 
      if(increment > 0 and current_num <= last):
         run_loop = True
      elif(increment < 0 and current_num >= last):
         run_loop = True
      else:
         run_loop = False
      
   return max_length, dec_length

# Run this calculation outside of the loop because it only
# needs to be done once
if(args.equalwidth == True):
   length = get_max_length(args.first, args.last, args.increment)

# Print the sequential numbers
# Using a while loop here instead of a for loop because python
# does not allow range to use floats

counter = args.first # Initializing count
run_loop = True
while(run_loop == True):

   # Print with equal character width using leading zeroes
   if args.equalwidth == True:
      print("{0:0{width}.{precision}f}".format(counter, width=length[0],
         precision=length[1]))

   # Print with special formatting
   elif args.string_format != None:
      print(args.string_format % counter)

   # Print with separator. See:
   # http://stackoverflow.com/questions/255147/
   #   how-do-i-keep-python-print-from-adding-spaces
   elif args.separator != None:
      print("{0:g}".format(counter), end='')
      print(args.separator, end="") 

   # Normal printing (no options)
   else:
      print("{0:g}".format(counter))

   # Increment by specified incrementer (defaults to 1)
   counter = counter + args.increment
   if(args.increment > 0 and counter <= args.last):
      run_loop = True
   elif(args.increment < 0 and counter >= args.last):
      run_loop = True
   else:
      run_loop = False
 
# Success!
exit(0)
