#!/usr/bin/env python2.7

# Copyright 2013 Kristina Frye
# CS 300
# sequ command, Compliance Level 2
# November 16, 2013 
#

# argparse allows us to easily parse the input arguments
from __future__ import print_function
import sys
import argparse
from decimal import Decimal

def get_version():
   return 'sequ version 1.10, written by Kristina Frye'

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
    
   # I am running a loop over all the numbers because some middle numbers
   # may need more decimal places than the first and last numbers. 
   while(run_loop == True):
      if(current_num.is_integer()):
         dec_length = 0
      else:
         dec_length = abs(Decimal(str(current_num)).as_tuple().exponent) 
      # The magic number '28' has been added below because sometimes
      # floating point representations aren't correct. We are
      # going to ignore representations more than 28 decimal places
      # and truncate them 
      if(max_dec_length < dec_length and dec_length < 28):
         max_dec_length = dec_length

      current_num += increment
      run_loop = continue_loop(current_num, last, increment)

   return max_dec_length
 
# This function gets the maximum width needed by the formatted number
# strings given a specified precision
def get_max_length(first, last, increment, precision):
   max_length = 0       
   current_num = first  
   run_loop = True

   while(run_loop == True):

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
   else:
      if(args.increment < 0):
         exit(0)

   # Limit the range so my computer doesn't run out of memory
   if(abs(args.last - args.first) > 100000000):
      print("The range between first and last must be less than 100000000.")
      exit(1) 

   if(args.pad != None):
      if((len(args.pad) == 2 and args.pad[0] != '\\') and len(args.pad) != 1):
         print("You need to specify a one character padding.")
         exit(1)

# This function prints the number sequence
def print_output(args):
   # Find the greatest decimal precision needed given the first and last
   # arguments and the increment. This is needed for correct printing
   # although we lose efficiency because it's using a loop
   # There's probably a better way to do this
   precision = get_max_precision(args.first, args.last, args.increment)

   # Find the formatted string width for -w, -p, or -P
   if(args.equalwidth == True or args.pad != None or args.padspaces == True):
      length = get_max_length(args.first, args.last, args.increment, precision)
      if(args.pad != None):
         pad = str(args.pad)
      elif(args.equalwidth == True):
         pad = '0'
      elif(args.padspaces == True):
         pad = ' '
      # The following alignment char '>' is needed for specifying the pad char
      pad += '>'
   
   # Find a specified separator for -s or -W 
   if(args.separator != None or args.words == True):
      if(args.separator != None):
         sep = args.separator
      else:
         sep = ' '
    
   current_num = args.first
   run_loop = True
   while(run_loop == True):

      # Print with specified width and precision (equal-width)
      if(args.equalwidth == True or args.pad != None or args.padspaces == True):
         print("{0:{fill}{width}.{prec}f}".format(current_num,
            fill=pad.decode('string_escape'),
            width=length, prec=precision)) 

      # Print with special formatting. We need a try here because the
      # format is coming directly from the user and may be incorrect
      elif args.string_format != None:
         try:
            print(args.string_format % current_num)
         except ValueError:
            print("That format is not accepted.")
            exit(1)

      # Print with separator. See:
      # http://stackoverflow.com/questions/255147/
      #   how-do-i-keep-python-print-from-adding-spaces
      # Print while evaluating backslash escapes:
      # http://stackoverflow.com/questions/4020539/process-escape-sequences-in-a-string-in-python
      elif args.separator != None or args.words == True:
         print("{0:g}".format(current_num), end='')
         print(sep.decode('string_escape'), end="") 

      # Normal printing (no options).
      else:
         print("{0:.{prec}f}".format(current_num, prec=precision))

      # Increment by specified incrementer (defaults to 1)
      current_num += args.increment
      
      # round to avoid bad floating point representations
      current_num = round(current_num, precision)
      run_loop = continue_loop(current_num, args.last, args.increment)
    
   # Success!
   exit(0)

########################################################################
# The following is the script that is always run with sequ

# Set up the parser
parser = argparse.ArgumentParser(description='The sequ command prints a '
   'sequence of numbers between the "first" and the "last" argument '
   'in increments of "increment," which defaults to 1.')
group = parser.add_mutually_exclusive_group()
parser.add_argument('first', 
   help='The starting integer (default=1)', type=float, nargs='?', default=1.0)
parser.add_argument('increment', 
   help='The increment between numbers (default=1)', 
   type=float, nargs='?', default=1.0)
parser.add_argument('last', help='The ending integer', type=float)
group.add_argument('-f', '--format', dest='string_format', 
   help='Print with special formatting: %%x, %%X, %%g, %%G, %%f, %%F', 
   nargs='?')
group.add_argument('-w', '--equal-width', dest='equalwidth',
   action='store_true', 
   help='Print all numbers with same width with zero padding, if necessary.')
group.add_argument('-s', '--separator', 
   help='Print with separator instead of each number on own line', nargs='?')
group.add_argument('-v', '--version', action='store_true',
   help='Print the version of the sequ program')
group.add_argument('-p', '--pad', 
   help='Pad to the left with the specified character', nargs='?')
group.add_argument('-P', '--pad-spaces', dest='padspaces', action='store_true',
   help='Pad to the left with spaces')
group.add_argument('-W', '--words', action='store_true', 
   help='Separate output with space instead of new line')

if(sys.argv[1] == '-v' or sys.argv[1] == '--version'):
   print(get_version())
   exit(0)
 
try:
   args = parser.parse_args()
except SystemExit:
   exit(1)

check_inputs(args)
print_output(args)
