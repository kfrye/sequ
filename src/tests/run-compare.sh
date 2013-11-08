#!/bin/sh

read args
while [ -n "$args" ]; do
   output_filename=`echo $args | sed 's/ /_/g'`
   echo -n "Test $args: "
   cmp $1.$output_filename $2.$output_filename
   if [ $? -eq 0 ]; then
      echo "passed"
   else
      echo "failed"
   fi
   read args
done 
