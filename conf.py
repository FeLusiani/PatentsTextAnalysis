from pathlib import Path

# PATHS
BASE_DIR        = Path.home() / Path('Projects/Microsoft_proj')
METADATA_DIR    = BASE_DIR / Path('metadata')
PDF_DIR         = BASE_DIR / Path('patents_pdf')
TXT_DIR         = BASE_DIR / Path('patents_txts')
CLEAN_TXT_DIR   = BASE_DIR / Path('cleaned_txt')
METADATA_CSV    = METADATA_DIR / Path('metadata.csv')
CACHE_DIR       = BASE_DIR / Path('cache')

# Read the README to see where to download the chrome driver
DRIVER_PATH     = BASE_DIR / Path('chromedriver')

# SCRAPER
YEARS = range(2013,2020+1)
ASSIGNEE = 'Microsoft'
LANG = 'ENGLISH'
PAGES_PER_YEAR = 1
RESULTS_PER_PAGE = 30

# DOWNLOADER
MAX_PDFS_PER_YEAR = 300

