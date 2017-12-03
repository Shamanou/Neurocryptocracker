#! /bin/bash
cd src
currencies=( "USD" "EUR" )
for element in "${currencies[@]}"
do
    ./train.py "$element" 
done
