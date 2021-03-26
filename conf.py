from pathlib import Path

# PATHS
BASE_DIR        = Path.home() / Path('Projects/IBM_proj')
METADATA_DIR    = BASE_DIR / Path('metadata')
PDF_DIR         = BASE_DIR / Path('patents_pdf')
TXT_DIR         = BASE_DIR / Path('patents_txts')
CLEAN_TXT_DIR   = BASE_DIR / Path('cleaned_txt')
METADATA_CSV    = METADATA_DIR / Path('metadata.csv')
CACHE_DIR       = BASE_DIR / Path('cache')

# Read the README to see where to download the chrome driver
DRIVER_PATH     = BASE_DIR / Path('chromedriver')

# SCRAPER
YEARS = range(2011,2012+1)
ASSIGNEE = 'IBM'
LANG = 'ENGLISH'

