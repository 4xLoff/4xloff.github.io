#!/bin/bash

echo "Enter the string to decode:"
read string

sus1='A-Za-z'
sus2='XYZA-xyzA-z'

decoded_string=$(echo "$string" | tr $sus1 $sus2)

echo "Original string: $string"
echo "Decoded string: $decoded_string"

