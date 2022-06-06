# Dog finder

A small project to find the word "dog" in PDFs with descriptions of medical experiments (on animals). The data comes from <https://eagri.cz>.

## Dependencies

- Python 3.6+
- `sips` to convert PDF to PNG
- [tesseract](https://tesseract-ocr.github.io/tessdoc/Home.html) with [Czech language](https://github.com/tesseract-ocr/tessdata/raw/main/ces.traineddata).
- [spacy](https://spacy.io/)

## How to use it

The idea is:

1. Convert PDF to PNG (because a PDF file contains a picture)
1. Run `tesseract` and get the text fromt he image.
1. Tokenize the text with `spacy`.
1. Find the word `pes`.
1. Write the results into `analysis.csv`.

Get processed text

```bash
. ./convert.sh <folder_with_pdfs>
```

> Calling `tesseract` directly worked better than Python wrapper during experimenting.

Analyse the data

```bash
python analyse.py
```
