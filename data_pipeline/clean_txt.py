from pathlib import Path
from multiprocessing import Pool
from functools import partial
import string
import argparse
import logging


import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, words
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

# if x in set is much faster than if x in list
stopwords_set = set(stopwords.words("english"))
# words_set = set(words.words())
punctuation_set = set(string.punctuation)

global porter, lemmatizer

def clean_str(in_str: str) -> str:
    """Cleans a string.

    Input string is tokenized. The tokens are iterated and added to the output,
    skipping unwanted tokens.
    """
    global porter, lemmatizer
    # split into words
    old_tokens = word_tokenize(in_str)
    new_tokens = []
    for token in old_tokens:
        if len(token) == 1:
            continue
        if token in stopwords_set:
            continue
        # if token in punctuation_set: continue
        if not token.isalpha():
            continue
        # if token not in words_set:continue
        # convert to lower case
        token = token.lower()
        # token = porter.stem(token)
        token = lemmatizer.lemmatize(token)
        new_tokens.append(token)

    return " ".join(new_tokens)


def clean_txt(file: Path, dest_dir: Path, overwrite=True):
    """Cleans a txt file.

    Args:
        file (Path): file to clean
        dest_dir (Path): directory where the ouput is saved
        overwrite (bool, optional): Overwrite output file if present. Defaults to True.
    """
    dest_file = dest_dir / Path(file.name)
    if not overwrite and dest_file.exists():
        logging.info(f"{file.name} present, skipping.")
        return

    with open(file, errors="replace") as f_stream:
        content = f_stream.read()

    content = clean_str(content)

    with open(dest_file, "w", errors="replace") as text_file:
        text_file.write(content)
    logging.info(f"{file.name} cleaned & saved")
    return


def batch_clean(src_dir: Path, dest_dir: Path, overwrite=True, multiproc=True):
    """Batch cleaning of txt files.
    Every file in src_dir is cleaned and saved in dest_dir.


    Args:
        src_dir (Path obj): dir containing txt files to be cleaned.
        dest_dir (Path obj): where cleaned txt files are saved.
        overwrite (bool, optional): If True (default), files in dest_dir will be overwritten.
        multiproc (bool, optional): If True (default), the function will use multiprocessing.
    """
    nltk.download("words")
    nltk.download("stopwords")
    nltk.download("punkt")
    nltk.download("wordnet")

    global porter, lemmatizer
    porter = PorterStemmer()
    lemmatizer = WordNetLemmatizer()

    dest_dir.mkdir(parents=True, exist_ok=True)
    files = src_dir.glob("*.txt")

    if multiproc:
        convert_func = partial(clean_txt, dest_dir=dest_dir, overwrite=overwrite)
        with Pool() as pool:
            pool.map(convert_func, files)
    else:
        for f in files:
            clean_txt(f, dest_dir, overwrite)

    return


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="Clean txts")
    arg_parser.add_argument("src_dir", help="dir with dirty txt files")
    arg_parser.add_argument("dst_dir", help="dir to save cleaned txt files")
    arg_parser.add_argument(
        "--no_overwrite", help="overwrite txts", action="store_true"
    )
    arg_parser.add_argument(
        "--no_multiproc", help="disable multiprocessing", action="store_true"
    )
    args = arg_parser.parse_args()

    porter = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    dst_dir = Path(args.dst_dir)
    src_dir = Path(args.src_dir)
    Path.mkdir(dst_dir, exist_ok=True)
    mp = not args.no_multiproc
    ov = not args.no_overwrite
    batch_clean(src_dir, dst_dir, ov, mp)
