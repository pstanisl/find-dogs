#!/bin/bash
folder=$1
for pdf in ${folder}/*.pdf; do
    echo "$pdf"
    sips -s format png --out "${pdf}.png" "$pdf"
    tesseract "${pdf}.png" "${pdf}" -l ces
done
