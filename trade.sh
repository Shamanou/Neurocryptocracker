#! /bin/bash
cd trader
currencies=( "USD" "EUR" )
for element in "${currencies[@]}"
do
    ./main.py hitbtc"$element" "$secret" "$key" "$userid"
done
