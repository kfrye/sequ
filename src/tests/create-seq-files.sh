#!/bin/sh 

read args
while [ -n "$args" ]; do
   output_filename=`echo $args | sed 's/ /_/g'`
   $1 $args > $1.$output_filename
read args
done
