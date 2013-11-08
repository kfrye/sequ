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

# This function determines if a loop should continue given the current number,
# the increment, and the last number
def continue_loop(current_num, last, increment):
   if(increment > 0 and current_num <= last):
      run_loop = True
   elif(increment < 0 and current_num >= last):
      run_loop = True
   else:
      run_loop = False
   return run_loop

# This function gets the maximum precision needed by the numbers
# It is only used when the equal-width option is selected
# http://stackoverflow.com/questions/6189956/easy-way-of-finding-decimal-places
def get_max_precision(first, last, increment):
   max_dec_length = 0
   current_num = first
   run_loop = True

   while(run_loop == True):
      if(current_num.is_integer()):
         dec_length = 0
      else:
         dec_length = abs(Decimal(str(current_num)).as_tuple().exponent) 
      
      if(max_dec_length < dec_length):
         max_dec_length = dec_length

      current_num += increment
      run_loop = continue_loop(current_num, last, increment)

   return max_dec_length
 
# This function gets the maximum width needed by the formatted number
# strings given a specified precision
def get_max_length(first, last, increment, precision):
   max_length = 0       #initialize the max lengths
   current_num = first  #initialize the current number 
   run_loop = True

   while(run_loop == True):

      # Calculate the string lengths and precision
      length = len("{0:.{prec}f}".format(current_num, prec=precision))

      if(max_length < length):
         max_length = length

      current_num += increment
      run_loop = continue_loop(current_num, last, increment)
 
   return max_length

# This function runs a few checks of the input for validity
def check_inputs(args):
   # Exit with success if nothing to print
   if(args.first > args.last):
      if(args.increment > 0):
         exit(0) 

   # Limit the range so my computer doesn't run out of memory
   if(abs(args.last - args.first) > 100000000):
      print("The range between first and last must be less than 100000000.")
      exit(1) 

# This function prints the number sequence
def print_output(args):

   # Find the formatted string width, if needed
   if(args.equalwidth == True):
      precision = get_max_precision(args.first, args.last, args.increment)
      length = get_max_length(args.first, args.last, args.increment, precision)

   current_num = args.first 
   run_loop = True
   while(run_loop == True):

      # Print with specified width and precision (equal-width)
      if args.equalwidth == True:
         print("{0:0{width}.{prec}f}".format(current_num, width=length,
            prec=precision)) 

      # Print with special formatting
      elif args.string_format != None:
         print(args.string_format % current_num)

      # Print with separator. See:
      # http://stackoverflow.com/questions/255147/
      #   how-do-i-keep-python-print-from-adding-spaces
      elif args.separator != None:
         print("{0:g}".format(current_num), end='')
         print(args.separator, end="") 

      # Normal printing (no options).
      # Find the decimal precision so that we can print it correctly without
      # rounding 
      else:
         if(current_num.is_integer()):
            print("{0:g}".format(current_num))
         else:  
            dec_length = abs(Decimal(str(current_num)).as_tuple().exponent)
            print("{0:.{precision}f}".format(current_num, precision=dec_length))

      # Increment by specified incrementer (defaults to 1)
      current_num += args.increment
      run_loop = continue_loop(current_num, args.last, args.increment)
    
   # Success!
   exit(0)

# Set up the parser
parser = argparse.ArgumentParser(description='The sequ command prints a '
   'sequence of numbers between the "first" and the "last" argument '
   'in increments of "increment," which defaults to 1.')

# We do not allow multiple simultaneous print options
group = parser.add_mutually_exclusive_group()

# Get first number. This is optional and defaults to 1
parser.add_argument('first', 
   help='The starting integer (default=1)', type=float, nargs='?', default=1.0)

# Get increment number. This is optional and defaults to 1
parser.add_argument('increment', 
   help='The increment between numbers (default=1)', 
   type=float, nargs='?', default=1.0)

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

check_inputs(args)
print_output(args)
