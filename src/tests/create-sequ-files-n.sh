#!/bin/sh

read args
while [ -n "$args" ]; do
   output_filename='n_'`echo $args | sed 's/ /_/g'`
   $1 '-n' $args > $1.$output_filename < 'test.txt'
read args
done
