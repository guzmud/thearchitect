#!/bin/bash
set -e

if [[ -z "$1" ]]; then
  echo "Missing first argument: pieces folder (input path)."
  exit 1
fi

if [[ -z "$2" ]]; then
  echo "Missing second argument: products folder (output path)."
  exit 1
fi

echo $1
echo $2
python3 /npi/thearchitect/conversion.py --pieces "$1" --products "$2"
