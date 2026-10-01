#!/usr/bin/bash

echo "Entrer un nombre: "
read -r num
echo "Nombre: $num"

if [ "$num" -gt 10 ]; then
  echo "Le nombre est plus grand que 10"
elif [ "$num" -eq 10 ]; then
  echo "Le nom est exactement 10"
else
  echo "Le nombre est plus petit que 10"
fi



