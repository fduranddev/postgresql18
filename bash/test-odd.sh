#!/usr/bin/bash

echo "Entrez un nombre: "
read -r num

if [ "$num" -gt 0 ]; then
  echo "$num est positif"
elif [ "$num" -lt 0 ]; then
  echo "$num est négatif"
else
  echo "$num est zéro"
fi