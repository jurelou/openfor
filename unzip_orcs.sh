#!/usr/bin/env bash

if test "$#" -ne 2; then
    echo Usage: $0 \<ORCS_FOLDER\> \<OUTPUT_FOLDER\>
    exit 1
fi

INPUT_FOLDER=$1
OUTPUT_FOLDER=$2

mkdir -p $OUTPUT_FOLDER

for file in $INPUT_FOLDER/*.7z; do
    [ -e "$file" ] || continue
    filename=$(basename -- "$file")
    echo Found 7z archive: $filename
    out_folder=$OUTPUT_FOLDER/${filename%.*}
    mkdir $out_folder
    7z x $file -o$out_folder > /dev/null


    for file2 in $out_folder/*.7z; do
        [ -e "$file2" ] || continue
        filename=$(basename -- "$file2")
        nested_out_folder=$out_folder/${filename%.*}
        mkdir -p nested_out_folder
        7z x $file2 -o$nested_out_folder > /dev/null
    done
done

echo Stored decompressed orcs in $OUTPUT_FOLDER