#! /bin/bash
cd trader
currencies=( "USD" "EUR" )
for element in "${currencies[@]}"
do
    ./main.py "$element" > log."$element"  2>&1 &
done
