#!/usr/bin/bash

if [[ $# -ne 1 ]]; then
    echo "pass day number"
    exit 1
fi

day=$1
solutionFile="solve${day}.py"
dayDirectory="day${day}"

mkdir "${dayDirectory}"
if [[ $? -ne 0 ]]; then
  echo "exiting"
  exit
fi

cd "${dayDirectory}"
ln -s ../common .

cp ../solveTemplate.py "${solutionFile}"

sed -i "s/DAY_NUM/${day}/g" "${solutionFile}"

touch exampleData.txt

echo "Day ${day} initialized."
