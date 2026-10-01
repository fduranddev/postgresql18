#!/usr/bin/bash

add() {
  local sum=$(($1 + $2))
  echo $sum
}

a=5
b=3

result=$(add "$a" "$b")
printf "La somme de %s et %s est %s\n" "$a" "$b" "$result"