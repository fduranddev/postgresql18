#!/usr/bin/bash

# Associative array example
declare -A colors
colors[apple]="red"
colors[banana]="yellow"
colors[grape]="purple"

unset "colors[banana]"
echo ${colors[apple]} # red
echo ${colors[grape]} # purple

declare -p colors