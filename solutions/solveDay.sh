#!/usr/bin/bash

if [[ $# -ne 2 ]]; then
    echo "pass input file name and day number"
    exit 1
fi

day=$2
input_file=$1

./solve"${day}".py ../input_puzzles/day"${day}"/"${input_file}"
