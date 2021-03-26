import requests
import glob
import pandas as pd
import progressbar
import time
from pathlib import Path
import argparse

def download_from_mtdt(metadata_dir:Path, pdf_dir:Path, overwrite=True, max_per_year=1e4):
    """Downloads the pdfs linked in the metadata files.

    Args:
        metadata_dir (Path): dir containing metadata files
        pdf_dir (Path): dir containing pdf files
        overwrite (bool, optional): Whether to overwrite existing pdfs.
            Defaults to True.
    """
    mtdt_files = metadata_dir.glob('*.csv')
    mtdt_files = list(mtdt_files)
    print('Will download pdfs from the following metadata files:')
    for file in mtdt_files:
        print(f'\t {file}')

    print(f'\n Overwrite existing pdfs: {overwrite} \n')
    for file in mtdt_files:
        df = pd.read_csv(file).head(max_per_year)
        year = df.loc[0,'Date_Priority'][:4]
        links = df.loc[:,'Link']

        print(f'Year: {year}')
        print(f'Metadata: {file.name}')
        print(f'Total urls: {len(links)}')

        print("\nExample urls:")
        for url in links[0:5]:
            print("\t" + url)
        print()

        start_time = time.time()
        bar_widgets = ["Downloading files...",
                        progressbar.Percentage(), progressbar.Bar()]
        bar = progressbar.ProgressBar(widgets=bar_widgets, maxval=len(links)).start()

        save_dir = pdf_dir / Path(year)
        save_dir.mkdir(parents=True, exist_ok=True)
        for i, url in enumerate(links):
            bar.update(i)

            filename = f'{year}_{i}.pdf'
            filepath = save_dir / Path(filename)
            if not overwrite and filepath.exists():
                continue

            download = requests.get(url)
            filepath.write_bytes(download.content)

        bar.finish()
        print(f"Time elapsed: {time.time() - start_time}s")
