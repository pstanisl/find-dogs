#!/bin/bash
year=$1
for pdf in ./data/${year}/*.pdf; do
    echo "$pdf"
    sips -s format png --out "${pdf}.png" "$pdf"
    tesseract "${pdf}.png" "${pdf}" -l ces
done
