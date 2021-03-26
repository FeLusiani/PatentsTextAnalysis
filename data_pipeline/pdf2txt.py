from tika import parser
import re
from pathlib import Path
import logging
from multiprocessing import Pool
from functools import partial


# 2 or more consecutive \s
spaces_regex = re.compile(r"\s{2,}")

def clean(txt: str) -> str:
    """Cleaning function applied to text.

    Used by `pdf_to_txt` on the text extracted, before saving to file.
    Can be edited to insert other text processing you wish to perform before saving.
    Args:
        txt (str): input text

    Returns:
        str: cleaned text.
    """
    # compact spaces
    txt = spaces_regex.sub(" ", txt)
    return txt


def pdf_to_txt(orig: Path, dest: Path = None, overwrite=True):
    """
    Converts a pdf file to txt.
    Args:
        orig (Path): path of pdf file
        dest (Path): directory where output txt is saved
        overwrite (bool): overwrite txt file (if present). Defaults to True.
    
    Returns False, if it could not convert successfully the pdf.
    """
    logging.info(f"Converting file {orig}")

    filename = orig.stem
    dest_file = dest / Path(filename + ".txt")

    if not overwrite and dest_file.exists():
        return True

    raw = parser.from_file(orig.as_posix())
    try:
        txt = raw["content"]
    except Exception:
        logging.warning(f" Could not convert: {orig}")
        return False
    
    # this happens if the pdf is a scan
    if txt is None or len(txt) < 300:
        logging.info(f" Did not save output text for {orig} (output length too small)")
        return False

    txt = clean(txt)
    with open(dest_file, "w", errors="replace") as text_file:
        text_file.write(txt)

    return True


def batch_convert(orig_dir:Path, dest_dir:Path=None, overwrite=True, multiproc=False):
    """
    Converts in txts the pdfs files contained in the `orig_dir` directory (and sub-directories) 
    Args:
        orig_dir (Path): directory to search for pdfs
        dest_dir (Path): directory where to save txts. By default, equals to `orig_dir`.
        overwrite (bool): if overrite=True (default), overwrites existing pdfs in `dest_dir`
        multiproc (bool): enable multiprocessing. Default is False.
    """
    if orig_dir.is_dir() is False:
        raise Exception(f"{orig_dir} is not an existing dir")
    if dest_dir is None:
        dest_dir = orig_dir

    logging.info(f" Batch converting - root folder: {orig_dir}")
    dest_dir.mkdir(parents=True, exist_ok=True)
    present_files = orig_dir.glob("**/*.pdf")
    present_files = list(present_files)

    if multiproc:
        convert_func = partial(pdf_to_txt, dest=dest_dir, overwrite=overwrite)
        pool = Pool(processes=4)
        results = pool.map(convert_func, present_files)
        pool.close()
        pool.join()
    else:
        results = []
        for f in present_files:
            r = pdf_to_txt(f, dest_dir, overwrite)
            results.append(r)

    logging.info(f" Number of successful convertions: {sum(results)}")