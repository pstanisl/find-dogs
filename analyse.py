import csv
import glob
import re
from functools import reduce
from os.path import basename, splitext
from typing import Any, List

from spacy.lang.cs import Czech


def get_images(pattern: str) -> str:
    """Get all the files in matching the pattern.

    Argiments:
        pattern (str) - glob pattern

    Return:
        generator with file paths
    """
    # yield "./data/_017_20.pdf.txt"
    for ipath in sorted(glob.glob(pattern)):
        yield ipath


def get_text(path: str) -> str:
    """Load text from a text file

    Arguments:
        path (str): path to the loaded file

    Return:
        string with lowered words without interpunction
    """
    text = []
    with open(path, "r", encoding="utf-8") as fr:
        for line in fr.readlines():
            line = re.sub("\W+", " ", line)
            line = line.strip()
            if not line:
                continue
            text.append(line)
        return " ".join(text).lower()


def tokenize(nlp, text: str) -> set:
    """Tokenize a text

    Arguments:
        nlp - an instance of the spacy languge
        text (str) - text to tokenize

    Return:
        a set with tokens
    """
    doc = nlp(text)
    return set([token.text for token in doc])


def check_dog(tokens: List[str]) -> bool:
    """Check tokens `pes`, `psi` or `psů` in a list with tokens

    Arguments:
        tokens (List[str]) - list with tokens

    Return:
        True if the token(s) is present in the tokens, otherwise False
    """
    return "pes" in tokens or "psi" in tokens or "psů" in tokens


def save(
    path: str, data: List[Any], header: List[str] = ["name", "is dog", "note"]
) -> None:
    """Save results into a CSV file.

    Arguments:
        path (str) - path to the output file
        data (List[Any]) - rows of the CSV
        header (List[str]) - header of the CSV (default: [name, is dog, note])
    """
    with open(path, "w", encoding="utf-8", newline="") as fw:
        writer = csv.writer(fw)
        writer.writerow(header)
        writer.writerows(data)


if __name__ == "__main__":
    results = []

    nlp = Czech()
    # Process all the text files in the data folder
    for n, ipath in enumerate(get_images("./data/**/*.txt")):
        text = get_text(ipath)

        tokens = tokenize(nlp, text)
        filename = splitext(basename(ipath))[0]
        is_dog = check_dog(tokens)

        print(f"{filename} - {is_dog}")

        results.append((filename, int(is_dog), ""))

    save("./analysis.csv", results)
    # Print some stats
    dogs_count = reduce(lambda prev, curr: prev + curr[1], results, 0)
    print(f"# of files: {len(results)}, # of dogs: {dogs_count}")
