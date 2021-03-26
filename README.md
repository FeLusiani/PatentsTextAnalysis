# Patents Text Analysis

Flexible, configurable code to perform web-scraping and text-mining on patents from Google Patents.

## Installation
```
git clone https://github.com/Maranc98/patents-nlp.git
cd ./patents-nlp
pip install -r requirements.txt
```

The web-scraping is performed using [Selenium](https://selenium-python.readthedocs.io/). You'll need to download the Chrome driver [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

Finally, configure the paths in [conf.py](./conf.py).



## Building the dataset 
Configure the assignee, the time range, and the language in [conf.py](./conf.py).
Then run `build_dataset.py` to build the dataset.

```
~/patents-nlp$ python build_dataset.py
usage: build_dataset.py [-h] [--delete] [--all] [--scrape] [--download] [--convert] [--clean] [--overwrite] [--multiproc]

scrape, download, convert and clean the data

optional arguments:
  -h, --help   show this help message and exit
  --delete     delete all data
  --all        execute whole pipeline
  --scrape     scrape metadata
  --merge      merge the scraped metadata
  --download   download pdfs using metadata
  --convert    convert pdfs to txts
  --clean      clean txts
  --overwrite  overwrite existing files
  --multiproc  use multiprocessing
  --verbose    show INFO logging
```

## Text Analysis

### Latent Semanantic Analysis (LSA)

### Fasttext

## Authors

* **Alessandro Marincioni** - [Maranc98](https://github.com/Maranc98)
* **Federico Lusiani** - [FeLusiani](https://github.com/FeLusiani)