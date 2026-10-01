#!/usr/bin/bash

greet() {
  local name=$1
  echo "Bonjour, $name!"
}
greet "Frederic"