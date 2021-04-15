# Patents Text Analysis

Flexible, configurable code to perform web-scraping and text-analysis on patents from Google Patents.

## Introduction
The code has been developed for a project to study IBM's patents (see below), but has been made perfectly general-purpose. Cloning this repository, you can easily build and analyze your own dataset, choosing the assignee and the years of publication.

## The IBM Patents dataset  [[link]](https://www.kaggle.com/federicolusiani/ibm-patents)
The code has been used to create the following dataset: [IBM Patents](https://www.kaggle.com/federicolusiani/ibm-patents).
The dataset contains the metadata and text of **~60K** patents assigned to IBM, through the years 2000-2019. The aim of this project was to find and study topics and trends in IBM technologies by performing text analysis. The plots shown below have been generated using just a small sample from this dataset, and serve as examples.

## Installation
```
git clone https://github.com/Maranc98/patents-nlp.git
cd ./patents-nlp
pip install -r requirements.txt
```

The web-scraping is performed using [Selenium](https://selenium-python.readthedocs.io/). You will need to download the Chrome driver [here](https://sites.google.com/a/chromium.org/chromedriver/downloads).

Finally, make sure to configure the paths in [conf.py](./conf.py).



## Building the dataset 
Configure the application paths and the scraping parameters in [conf.py](./conf.py).
In particular, the scraping parameters are:
- Assignee's name
- Years range
- Language
- Number of result pages to scrape per month
- Number of patents per page


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

The pipeline for building the dataset  is the following:

- Using the search criteria listed above, metadata of the patents is scraped from Google Patents, saving each year in its own `.csv` file.
- The metadata files are merged in a single `.csv` file.
- The patents listed in the unified `.csv` file are downloaded (as `.pdf` files).
- The `.pdf` files are converted to `.txt` by performing OCR with the [tika](https://github.com/chrismattmann/tika-python) python library.
- The `.txt` files are cleaned using the `nltk` python library: stop-words and punctuation removal, lemmification of tokens.

## Latent Semantic Analysis (LSA)

The code in [lsa_example.ipynb](./lsa_example.ipynb) shows how to perform a latent semantic analysis of the text corpus using the functions in the module `LSA`.

The code performs TFIDF on the text corpus, and then factorizes the words_documents matrix (using either SVD or NMF method), yielding the words- and documents- embedding of the latent topics.

![plot from lsa output](./images/2019_NMF_T15.png)

The plot shows the top 15 topics found in the text corpus (in this case, a sample from IBM's patents published in the year 2019). For each topic, the top 4 words are shown.

## Analyzing the trends of chosen topic
In the [topics_trends.ipynb](./topics_trends.ipynb) notebook, we perform an analysis of the trends of hand-made topics (sets of keywords) to study how their frequency changes through the years.

```
Medicine
 - Keywords: ['medical', 'patient', 'health', 'treatment']
ML
 - Keywords: ['neural', 'train', 'recognition', 'learn']
Aut. driving
 - Keywords: ['vehicle', 'autonomous', 'park']
Quantum comput.
 - Keywords: ['quantum']
```
![](./images/trends_plot.svg)

## Authors

* **Alessandro Marincioni** - [Maranc98](https://github.com/Maranc98)
* **Federico Lusiani** - [FeLusiani](https://github.com/FeLusiani)
