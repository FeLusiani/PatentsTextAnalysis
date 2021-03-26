import argparse
from shutil import rmtree
import logging
from pathlib import Path

from data_pipeline.scraper import make_driver, scrape_metadata
from data_pipeline.pdf_download import download_from_mtdt
from data_pipeline.pdf2txt import batch_convert
from data_pipeline.clean_txt import batch_clean
from utils.utils import merge_csv_files

from conf import DRIVER_PATH, METADATA_DIR, YEARS, ASSIGNEE, LANG
from conf import MAX_PDFS_PER_YEAR, PAGES_PER_YEAR, RESULTS_PER_PAGE
from conf import PDF_DIR, TXT_DIR, CLEAN_TXT_DIR, METADATA_CSV


arg_parser = argparse.ArgumentParser(
    description="scrape, download, convert and clean the data"
)

# pipeline
arg_parser.add_argument("--delete", help="delete all data", action="store_true")
arg_parser.add_argument("--all", help="execute whole pipeline", action="store_true")
arg_parser.add_argument("--scrape", help="scrape metadata", action="store_true")
arg_parser.add_argument("--merge", help="merge the scraped metadata", action="store_true")
arg_parser.add_argument("--download", help="download pdfs using metadata", action="store_true")
arg_parser.add_argument("--convert", help="convert pdfs to txts", action="store_true")
arg_parser.add_argument("--clean", help="clean txts", action="store_true")

# modes
arg_parser.add_argument(
    "--overwrite", help="overwrite existing files", action="store_true"
)
arg_parser.add_argument("--multiproc", help="use multiprocessing", action="store_true")


arg_parser.add_argument("--verbose", help="show INFO logging", action="store_true")

args = arg_parser.parse_args()

if args.verbose:
    logging.basicConfig(level=logging.INFO)

if args.delete:
    dirs = [METADATA_DIR, PDF_DIR, TXT_DIR, CLEAN_TXT_DIR]
    [rmtree(d,ignore_errors=True) for d in dirs]

if args.all or args.scrape:
    METADATA_DIR.mkdir(parents=True,exist_ok=True)
    driver = make_driver(DRIVER_PATH)
    for y in YEARS:
        save_path = METADATA_DIR / Path(str(y) + '_patents.csv')
        scrape_metadata(ASSIGNEE, y, LANG, driver, save_path, PAGES_PER_YEAR, RESULTS_PER_PAGE)

if args.all or args.merge:
    merge_csv_files(METADATA_DIR, METADATA_CSV)

if args.all or args.download:
    download_from_mtdt(METADATA_DIR, PDF_DIR, args.overwrite, MAX_PDFS_PER_YEAR)

if args.all or args.convert:
    batch_convert(PDF_DIR, TXT_DIR, args.overwrite, args.multiproc)

if args.all or args.clean:
    batch_clean(TXT_DIR, CLEAN_TXT_DIR, args.overwrite, args.multiproc)

