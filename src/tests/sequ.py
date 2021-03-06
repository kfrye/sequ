#!/usr/bin/env python2.7

# Copyright 2013 Kristina Frye
# CS 300
# sequ command, Compliance Level 3 and 4 
# December 2, 2013 
#

# argparse allows us to easily parse the input arguments
from __future__ import print_function
import sys
import argparse
from decimal import Decimal
import roman
import pdb

def get_version():
   return 'sequ version 1.30, written by Kristina Frye'

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
# http://stackoverflow.com/questions/6189956/easy-way-of-finding-decimal-places
def get_max_precision(first, last, increment):
   if(first.is_integer()):
      max_dec_length = 0
   else:
      max_dec_length = abs(Decimal(str(first)).as_tuple().exponent)

   if(last.is_integer() == False):
      dec_length = abs(Decimal(str(last)).as_tuple().exponent)
      if(dec_length > max_dec_length):
         max_dec_length = dec_length

   if(increment.is_integer() == False):
      dec_length = abs(Decimal(str(increment)).as_tuple().exponent)
      if(dec_length > max_dec_length):
         max_dec_length = dec_length
 
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

# This function gets the maximum width needed by a sequence of roman
# numbers
def get_max_length_roman(first, last, increment):
   max_length = 0
   current_num = int(first)
   run_loop = True

   while(run_loop == True):
      roman_str = roman.toRoman(current_num)
      length = len(roman.toRoman(current_num))

      if(max_length < length):
         max_length = length

      current_num += int(increment)
      run_loop = continue_loop(current_num, last, increment)

   return max_length

# Get the maximum length of character strings
def get_max_length_alpha(first, last, input_type):
   first_length = len(getCharString(first, input_type))
   last_length = len(getCharString(last, input_type))
   if(first_length > last_length):
      max_length = first_length
   else:
      max_length = last_length
   return max_length

# Determine if a given string parses as a roman numeral 
def isRoman(s):
   if roman.romanNumeralPattern.search(s):
      return True
   else:
      return False

# Determine if a given string is an uppercase roman numeral
def isUpperRoman(s):
   if isRoman(s.upper()) and isUpperAlpha(s):
      return True
   return False

# Determine if a given string is a lowercase roman numeral
def isLowerRoman(s):
   if isRoman(s.upper()) and isLowerAlpha(s):
      return True
   return False 

# How to determine string is a number:
# http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-in-python 
def isFloat(input_string):
   try:
      float(input_string)
      return True
   except ValueError:
      return False

# Determine if a string is an integer
def isInteger(input_string):
   if(isFloat(input_string)):
      if(float(input_string).is_integer()):
         return True
   return False

# Determine if a string is upper-case alpha
def isUpperAlpha(input_string):
   if(str(input_string).isupper()):
      return True
   return False

# Determine if a string is lower-case alpha
def isLowerAlpha(input_string):
   if(str(input_string).islower()):
      return True
   return False

# Takes a string and returns 'R' for upper case roman, 'r' for lower case
# roman, 'A' for upper case alpha, 'a' for lower case alpha, 'i' for integer, 
# 'f' for float, and '0' for none of the above, Since alpha always has
# preference over roman, roman is never set as the default type
def getType(s):
   if(isInteger(s)):
      return 'i'
   elif(isFloat(s)):
      return 'f'
   elif(s.isupper()):
      return 'A'
   elif(s.islower()):
      return 'a'
   else:
      return '0'

# Converts a character string into a numeric string 
def fromCharString(s):
   length = len(s)
   num = ord('a') - 1
   
   for i in range(length - 1, -1, -1):
      letter = ord(s[i]) - ord('a') + 1
      letter = letter * 26**(length - i - 1)
      num += letter

   return num

# Converts a numeric string into a character string
def getCharString(num, input_type):
   # We can't have negative characters, so use 'a' or 'A' for numbers
   # decremented below a 
   if(num < ord('a') and input_type == 'a' or
      num < ord('A') and input_type == 'A'):
      return input_type 
   if(input_type == 'A'):
      num = ord(chr(num).lower())
   num -= ord('a')
   char_string = getLetter(num, False)
   if(input_type == 'A'):
      char_string = char_string.upper()
   return char_string

# Converts a string to a number based upon the input type of the string
def convertToNum(input_type, s):
   if(input_type == 'R'):
      num = roman.fromRoman(s)
   elif(input_type == 'r'):
      num = roman.fromRoman(s.upper())
   elif(input_type == 'a' or input_type == 'A'):
      num = fromCharString(s.lower()) 
   elif(input_type == 'i' or input_type == 'f'):
      num = float(s)
   else:
      num = 0
   return num

# Class used to store the type and numeric value of a number 
class SequValue:
   def __init__(self, s):
      self.input_string = s
      self.value_type = getType(s)
      self.num = convertToNum(self.value_type, s)

   def setType(self, input_type):
      if(self.value_type != 'i'):
         self.num = convertToNum(input_type, self.input_string)
      self.value_type = input_type

# Returns a roman numeral string based upon a number and the type 
# (lower case vs upper case roman)
def getRomanString(num, input_type):
   # This error checking handles the occasion when the number is too big
   # (> 4999) or too small (< 1) to be converted to a roman numeral.
   try:
      roman_str = roman.toRoman(int(num))
   except roman.RomanError:
      if(input_type == 'r'):
         return 'i'
      else:
         return 'I'

   if(input_type == 'R'):
      return roman_str 
   else:
      return roman_str.lower()

# Returns a string to be used with equal-width printing
def getEqualWidthString(value_type, current_num, pad, length, precision):
   if(value_type == 'f' or value_type == 'i'):
      output_string = "{0:{fill}{width}.{prec}f}".format(current_num,
         fill=pad.decode('string_escape'),
         width=length, prec=precision)
   elif(value_type == 'R' or value_type == 'r'):
      output_string="{0:{fill}{width}}".format(getRomanString(current_num,
         value_type), fill=pad, width=length)
   else:
      output_string = "{0:{fill}{width}}".format(getCharString(int(current_num),
         value_type), fill=pad, width=length)
   return output_string

# Returns string without special formatting
def getNormalString(value_type, current_num, precision):
   if(value_type == 'f' or value_type == 'i'):
      output_string = "{0:.{prec}f}".format(current_num, prec=precision)
   elif(value_type == 'R' or value_type == 'r'):
      output_string = getRomanString(current_num, value_type)
   else:
      output_string = getCharString(int(current_num), value_type)
   return output_string

# Recursive function used to get a character sequence from a number.
# Repeat is set to false when called outside of the function
def getLetter(num, repeat):
   if(repeat == True):
      num -= 1

   if(num <= 25):
      letter = chr(num + ord('a'))
      return letter

   return_string = getLetter(int(num / 26), True)
   return_string += chr((num % 26) + ord('a'))
   return return_string

# Returns a SequValue object with defaults appropriate for a beginning
# value for the type. For instance, type 'A' should begin with a capital 'A'
def setDefaults(value_type):
   if(value_type == 'r' or value_type == 'R' or value_type == 'i' or 
      value_type == 'f'): 
      default = SequValue('1') 
   elif(value_type == 'a'): 
      default = SequValue('a')
   elif(value_type == 'A'):
      default = SequValue('A')
   return default

# This function is used when format_word is specified. It checks that
# all the arguments will work with the format_word
def parseFormatWord(args, first, last, increment):
   isParsed = True
   format_word = args.format_word
   value_type = last.value_type

   #print("Value type: ", value_type)
   # If roman, check that the arguments can parse as roman
   if(format_word == 'roman' or format_word == 'ROMAN'):
      if((isUpperRoman(args.last) == True and format_word == 'ROMAN') or
         (last.value_type == 'i' and format_word == 'ROMAN')):
         value_type = 'R'
      
      elif((isLowerRoman(args.last) == True and format_word == 'roman') or
         (last.value_type == 'i' and format_word == 'roman')):
         value_type = 'r'
      
      else:
         isParsed = False

      # The first and increment arguments can also be integer 
      if(args.first != None and first.value_type != 'i'):
         if((value_type == 'r' and isLowerRoman(args.first) == False) or
            (value_type == 'R' and isUpperRoman(args.first) == False)):
            isParsed = False

      if(args.increment != None and increment.value_type != 'i'):
         if((value_type == 'r' and isLowerRoman(args.increment) == False) or
            (value_type == 'R' and isUpperRoman(args.increment) == False)):
            isParsed = False

   # If alpha, check that the arguments can parse as alpha
   elif(format_word == 'alpha' or format_word == 'ALPHA'):
      if(isUpperAlpha(args.last) and format_word == 'ALPHA'):
         value_type = 'A'
      elif(isLowerAlpha(args.last) and format_word == 'alpha'):
         value_type = 'a'
      # When using number-lines option, make sure to use the type of the 
      # 'first' argument since we don't care about the type of 'last'
      elif(args.nlines == True and 
         (first.value_type == 'a' or first.value_type == 'A')):
         value_type = first.value_type
      else:
         isParsed = False

      if(args.first != None):
         if((value_type == 'a' and isLowerAlpha(args.first) == False) or 
            (value_type == 'A' and isUpperAlpha(args.first) == False)):
            isParsed = False
      
      # The increment argument for alpha must be integer
      if(args.increment != None):
         if(increment.value_type != 'i'):
            isParsed = False

   # If arabic, check that all the other arguments are also integer
   elif(format_word == 'arabic'):
      if(last.value_type != 'i'):
         isParsed = False
      else:
         value_type = 'i'

      if(args.first != None and first.value_type != 'i'):
         isParsed = False

      if(args.increment != None and increment.value_type != 'i'):
         isParsed = False

   # If floating, check that all the other arguments can be parsed as floats
   elif(format_word == 'floating'):
      if(isFloat(args.last) == True):
         value_type = 'f'
      else:
         isParsed = False

      if(args.first != None and isFloat(args.first) == False):
         isParsed = False

      if(args.increment != None and isFloat(args.increment) == False):
         isParsed = False

   else:
      print("That format word is not recognized.")
      exit(1)

   # Return whether arguments passed checks and the input_type for the
   # last argument
   return isParsed, value_type


# This function runs a few checks of the input for validity
def check_inputs(args):
   # Create objects for first, last, and increment that store the
   # string, type, and numeric value of each number. 
   last = SequValue(args.last)
   if(last.value_type == '0'):
      print('The "last" value is not valid')
      exit(1)

   if(args.first != None):
      first = SequValue(args.first)
   else:
      first = setDefaults(last.value_type)

   if(args.increment != None):
      increment = SequValue(args.increment)
   else:
      increment = SequValue("1") 

   if(args.format_word != None):
      # Check the arguments and the format word agree
      parse_format_word = parseFormatWord(args, first, last, increment)
      if(parse_format_word[0] == False):
         print("The arguments do not agree with the specified format word")
         exit(1)
      else:
         # If changing from an int to roman, change the format, but not the
         # value. When changing from an alpha to a roman, change both
         # setType changes both. 
         if(last.value_type == 'i' and 
            (parse_format_word[1] == 'r' or parse_format_word[1] == 'R')):
            last.value_type = parse_format_word[1] 
            print("Value type: ", last.value_type)
         else:   
            last.setType(parse_format_word[1])

         # If we changed the format type to roman, make sure the 
         # first and increment format types are also set to roman
         if(last.value_type == 'r'):
            if(args.first != None):
               first.setType('r')
            if(args.increment != None):
               increment.setType('r')
            if(args.first == None):
               first = setDefaults('r')

         elif(last.value_type == 'R'):
            if(args.first != None):
               first.setType('R')
            if(args.increment != None):
               increment.setType('R')
            if(args.first == None):
               first = setDefaults('R') 

   # Set a flag in order to combine error messages later
   not_matching = False

   # Check arguments when last is an alpha 
   if(last.value_type == 'a' or last.value_type == 'A'):
      if(args.first != None):
         if(first.value_type != last.value_type):
            not_matching = True

      if(args.increment != None):
         if(increment.value_type != 'i'):
            print("Alpha arguments must use an arabic (integer) increment")
            exit(1)

      if(args.string_format != None):
         print("Alpha arguments cannot be used with the special format option.")
         exit(1)

   # Check arguments when last is an int 
   elif(last.value_type == 'i' and args.nlines == False):
      if(args.first != None):
         if(first.value_type != 'i' and first.value_type != 'f'):
            not_matching = True

      if(args.increment != None):
         if(increment.value_type != 'i' and increment.value_type != 'f'):
            not_matching = True

   # Check arguments when last is a float
   elif(last.value_type == 'f'):
      if(args.first != None):
         if(first.value_type != 'i' and first.value_type != last.value_type):
            not_matching = True

      if(args.increment != None):
         if(increment.value_type != last.value_type and 
            increment.value_type != 'i'):
            not_matching = True

   # This combines some error messages found above
   if(not_matching == True):
      print("The limit arguments must be of the same type")
      exit(1)

   # Check arguments when last is roman
   elif(last.value_type == 'r' or last.value_type == 'R'):
      if(last.num > 4999 or first.num > 4999 or increment.num > 4999):
         print("Roman numbers may only be used with numbers up to 4999.")
         exit(1)
      if(args.string_format != None):
         print("Roman numbers cannot be used with the special format option.")
         exit(1)

   # When number-lines option is specified, we want to use the format type
   # of the 'first' argument instead of the 'last' argument, so we fake
   # it out this way. 
   if(args.nlines == True):
      last.value_type = first.value_type

   # Exit with success if nothing to print
   if(first.num > last.num and args.nlines == False):
      if(increment.num > 0):
         exit(0) 
   else:
      if(increment.num < 0 and args.nlines == False):
         exit(0)

   # Limit the range so my computer doesn't run out of memory
   if(abs(last.num - first.num) > 100000000):
      print("The range between first and last must be less than 100000000.")
      exit(1) 

   # Don't allow equal-width or pad options when numbers-lines is specified
   # since the ending number is undetermined.  
   if((args.equalwidth == True or args.pad != None or args.padspaces == True or
      args.words == True) 
      and args.nlines == True):
      print("You can't use the 'pad,' 'pad-spaces,' 'equal-width,' or 'words'"+
         " options with the print-lines option.")
      exit(1) 

   # limit pad characters, but allow backslash escapes by checking for
   # two character pad in which the first character is '\'
   if(args.pad != None):
      if((len(args.pad) == 2 and args.pad[0] != '\\') and len(args.pad) != 1):
         print("You need to specify a one character padding.")
         exit(1)
   return first, last, increment



# This function prints the number sequence
def print_output(args, inputs):
   first = inputs[0]
   last = inputs[1]
   increment = inputs[2]

   # Find the greatest decimal precision needed given the first and last
   # arguments and the increment. This is needed for correct printing
   # although we lose efficiency because it's using a loop
   # There's probably a better way to do this
   if(last.value_type == 'f' or last.value_type == 'i'):
      precision = get_max_precision(first.num, last.num, increment.num)
   else:
      precision = 1
 
   # Find the formatted string width for -w, -p, or -P
   if(args.equalwidth == True or args.pad != None or args.padspaces == True):
      if(last.value_type == 'f' or last.value_type == 'i'):   
         length = get_max_length(first.num, last.num, increment.num, precision)
      elif(last.value_type == 'r' or last.value_type == 'R'):
         length = get_max_length_roman(first.num, last.num, increment.num)
      elif(last.value_type == 'a' or last.value_type == 'A'):
         length = get_max_length_alpha(first.num, last.num, last.value_type)

      if(args.pad != None):
         pad = str(args.pad)
      elif(args.equalwidth == True):
         if(last.value_type == 'f' or last.value_type == 'i'):
            pad = '0'
         elif(last.value_type == 'r' or last.value_type == 'R' or
              last.value_type == 'a' or last.value_type == 'A'):
            pad = ' '
      elif(args.padspaces == True):
         pad = ' '
      # The following alignment char '>' is needed for specifying the pad char
      pad += '>'
 
   # Find a specified separator for -s or -W 
   if(args.separator != None or args.words == True or args.nlines == True):
      if(args.separator != None):
         sep = args.separator
      else:
         sep = ' '
    
   current_num = first.num
   run_loop = True
   while(run_loop == True):

      value_type = last.value_type
      # Print with specified width and precision (equal-width)
      if(args.equalwidth == True or args.pad != None or args.padspaces == True):
         output_string = getEqualWidthString(value_type, current_num, pad,
            length, precision)

      # Print with special formatting. We need a try here because the
      # format is coming directly from the user and may be incorrect
      elif args.string_format != None:
         try:
            output_string = args.string_format % current_num
         except ValueError:
            print("That format is not accepted.")
            exit(1)

      # Print with floating specified. This will print with decimal point 
      elif(args.format_word == 'floating'):
         output_string = str(current_num)

      # Normal printing (no options).
      else:
         output_string = getNormalString(value_type, current_num, precision)

      # When using separator or print-lines, we want to be able to append
      # the separator (or stdin line) to the number instead of starting
      # a new line right away
      if(args.separator != None or args.words == True or args.nlines == True):
         output_string += sep.decode('string_escape')
         if(args.nlines == True):
            line = sys.stdin.readline()
            if line:
               output_string += line

            # exit when stdin is complete. This is done here so that we
            # don't print a number with an empty line 
            else:
               exit(0) 
         print(output_string, end="")
      else:
         print(output_string)

      # Increment by specified incrementer (defaults to 1)
      current_num += increment.num
      
      # round to avoid bad floating point representations
      current_num = round(current_num, precision)

      # Check if we should go to the next loop. When number-lines is 
      # specified, this is always true. The exit for that option is
      # above
      if(args.nlines == False):
         run_loop = continue_loop(current_num, last.num, increment.num)
       
   # Success!
   exit(0)

# This class is used to parse the input arguments and assign them to
# "first," "last," and "increment," depending upon which arguments are
# specified. This allowed me to implement CL4 with only small changes
# needed to the rest of the program
class ParsedArgs:
   def __init__(self, args):
      self.first = args.first
      self.last = args.last
      self.increment = args.increment
      self.nlines = args.nlines
      self.format_word = args.format_word
      self.string_format = args.string_format
      self.equalwidth = args.equalwidth
      self.separator = args.separator
      self.pad = args.pad
      self.padspaces = args.padspaces
      self.words = args.words
      if(args.first == None):
         if(args.nlines == False):
            print("Either the 'last' argument or -n (used with stdin) needs "+
               "to be specified.")
            exit(1)
         else:
            self.last = '1'

      elif(args.first != None and args.nlines == True):
         if(args.last != None):
            print("The 'last' argument cannot be specified at the same time "+
               "as the --number-lines option is used.")
            exit(1)
         else:
            self.last = '1'

      elif(args.increment == None):
         self.first = None
         self.last = args.first
      elif(args.last == None):
         self.last = args.increment
         self.increment = None
           

########################################################################
# The following is the script that is always run with sequ

# Set up the parser
parser = argparse.ArgumentParser(description='The sequ command prints a '
   'sequence of numbers between the "first" and the "last" argument '
   'in increments of "increment," which defaults to 1.')
group = parser.add_mutually_exclusive_group()
parser.add_argument('first', 
   help='The starting integer (default=1)', nargs='?')
parser.add_argument('increment', 
   help='The increment between numbers (default=1)', nargs='?')
parser.add_argument('last', help='The ending integer', nargs='?')
parser.add_argument('-n', '--number-lines', dest='nlines', action='store_true',
   help="Add numbers to stdin and output to stdout.")
parser.add_argument('-F', '--format_word', 
   help='Print with arabic (for integers), floating, alpha (for characters), '+ 
   'ALPHA (for capital characters), roman (for roman numerals), ROMAN (for '+
   'capital roman numerals).') 
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

try:
   if(sys.argv[1] == '-v' or sys.argv[1] == '--version'):
      print(get_version())
      exit(0)
   args = parser.parse_args()

# This exception is thrown if no arguments are given
except IndexError:
   print("Use sequ -h for help.")
   exit(1)
except SystemExit:
   exit(1)

pargs = ParsedArgs(args)
#print("First: ", pargs.first)
#print("Last: ", pargs.last)
#print("Increment: ", pargs.increment)
inputs = check_inputs(pargs)
print_output(pargs, inputs)
