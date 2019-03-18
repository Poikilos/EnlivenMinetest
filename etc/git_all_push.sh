#!/bin/sh

# Before doing this, you can try:
#   git diff

if [ ! -z "$1" ]; then
  if [ -z "$2" ]; then
    echo "git add -A"
    git add -A
    echo "git commit -m \"$1\""
    git commit -m "$1"
    echo "git push"
    git push
  else
    echo "Too many arguments. Specify only a message, in quotes."
  fi
else
  echo "You must specify a message in quotes."
fi
