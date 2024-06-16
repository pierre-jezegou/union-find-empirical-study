#!/bin/bash

TEX_DIR="."

if [ ! -d "$TEX_DIR" ]; then
  echo "The specified directory does not exist: $TEX_DIR"
  exit 1
fi

for texfile in "$TEX_DIR"/*.tex; do
  if [ -f "$texfile" ]; then
    echo "Compiling $texfile..."
    tectonic "$texfile"
    
    if [ $? -ne 0 ]; then
      echo "Error compiling $texfile"
    else
      echo "Successfully compiled $texfile"
    fi
  else
    echo "No .tex files found in $TEX_DIR"
  fi
done

echo "Compilation finished."