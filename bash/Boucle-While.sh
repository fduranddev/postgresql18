#!/usr/bin/bash

count=1
while [ $count -le 5 ]; do
  echo "Le compteur est: $count"
  ((count++))
done