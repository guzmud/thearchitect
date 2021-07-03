#!/bin/bash
set -e

if [[ -z "$1" ]]; then
  echo "Missing first argument (input path)."
  exit 1
fi

if [[ -z "$2" ]]; then
  echo "Missing second argument (output path)."
  exit 1
fi

x86_64-w64-mingw32-gcc -o "$2" "$1"
