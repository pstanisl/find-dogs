import csv
import glob
import re
from functools import reduce
from os.path import basename, splitext
from typing import Any, List

import cv2
from spacy.lang.cs import Czech


def get_images(pattern: str) -> str:
    # yield "./data/_017_20.pdf.txt"
    for ipath in sorted(glob.glob(pattern)):
        yield ipath


def load_image(path: str) -> cv2.Mat:
    return cv2.imread(path)


def get_text(path: str) -> str:
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
    doc = nlp(text)
    return set([token.text for token in doc])


def check_dog(tokens: List[str]) -> bool:
    return "pes" in tokens or "psi" in tokens or "psů" in tokens


def save(
    path: str, data: List[Any], header: List[str] = ["name", "is dog", "note"]
) -> None:
    with open(path, "w", encoding="utf-8", newline="") as fw:
        writer = csv.writer(fw)
        writer.writerow(header)
        writer.writerows(data)


if __name__ == "__main__":
    results = []

    nlp = Czech()

    for n, ipath in enumerate(get_images("./data/**/*.txt")):
        text = get_text(ipath)

        tokens = tokenize(nlp, text)
        filename = splitext(basename(ipath))[0]
        is_dog = check_dog(tokens)

        print(f"{filename} - {is_dog}")

        results.append((filename, int(is_dog), ""))

    save("./analysis.csv", results)

    dogs_count = reduce(lambda prev, curr: prev + curr[1], results, 0)
    print(f"# of files: {len(results)}, # of dogs: {dogs_count}")
