import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from pathlib import Path
import matplotlib.pyplot as plt


def df_from_txts(txts_dir):
    """Generate dataframe from txt files in a directory.

    Index "ID" will be the name of the txt file (stripped of the ".txt").
    Column "Text" is the file content.

    Args:
        txts_dir (Path): directory containing the txt files

    Returns:
        pandas.Dataframe: dataframe. Index: "ID", Columns: "Text"
    """

    file_list = txts_dir.glob("**/*.txt")
    doc_texts = {}

    for f in file_list:
        filename = f.stem
        with open(f, errors="replace") as f_stream:
            content = f_stream.read()
        doc_texts[filename] = content

    df = pd.DataFrame.from_dict(doc_texts, orient="index", columns=["Text"])
    df.index.names = ["ID"]
    return df


def merge_csv_files(csv_dir: Path, csv_result: Path):
    """Appends all the csv files inside of `csv_dir` (and sub-directories)
    into one `csv_result` file.
    """

    csv_list = csv_dir.glob("**/*.csv")
    combined_df = pd.concat([pd.read_csv(f) for f in csv_list])
    combined_df.to_csv(csv_result, index=False)


def add_year_column(df, csv_metadata):
    """Add the "Year" column to the patents dataframe `df`.

    Args:
        df (pandas.Dataframe): Dataframe with "ID" index or column.
        csv_metadata (Path): csv file, with "Name" and "Date_Priority" columns.

    Returns:
        pandas.Dataframe: dataframe. Index: "ID", Columns: "Text", "Year"
    """
    df2 = pd.read_csv(csv_metadata, usecols=["Name", "Date_Priority"])
    df2["Name"] = df2["Name"].str[:-4]  # delete ".pdf"
    df2 = df2.rename(columns={"Date_Priority": "Year"})
    df2["Year"] = df2["Year"].str[:4]  # extract year from date

    df2.set_index("Name", inplace=True)
    df2.index.name = "ID"

    # left join on ID with df
    df = df.merge(df2, how="left", on="ID")
    return df


def add_month_column(df, csv_metadata):
    """Add the "Month" column to the patents dataframe df.

    Args:
        df (pandas.Dataframe): Dataframe with "ID" index or column.
        csv_metadata (Path): csv file, with "Name" and "Date_Priority" columns.

    Returns:
        pandas.Dataframe: dataframe. Index: "ID", Columns: "Text", "Month"
    """
    df2 = pd.read_csv(csv_metadata, usecols=["Name", "Date_Priority"])
    df2["Name"] = df2["Name"].str[:-4]  # delete ".pdf"
    df2 = df2.rename(columns={"Date_Priority": "Month"})
    df2["Month"] = df2["Month"].str[:7]  # extract year and month from date

    df2.set_index("Name", inplace=True)
    df2.index.name = "ID"

    # left join on ID with df
    df = df.merge(df2, how="left", on="ID")
    return df


def get_topics_count(text_corpus, topics, max_count: int = None):
    """For every topic, returns frequency in the text corpus.

    Topic frequency = mean of topic keywords occurences.
    Occurences of a keyword are counted for every text in the corpus,
    capped at max_count (if set), and summed together.

    Args:
        txts (list): text corpus, given as list of texts.
        topics (dictionary): Key is topic name, Value is a list of the topic keywords.
        max_count (int): if set, keyword count per text in corpus is capped at max_count.

    Returns:
        list: occurences per topic.
    """
    # concatenate topics keywords in one list
    # so we can apply CountVectorizer just once (better performance)
    words = []
    for t in topics:
        words += topics[t]

    counter_vectorizer = CountVectorizer(vocabulary=words)
    txt_word_matrix = counter_vectorizer.fit_transform(text_corpus)
    word_txt_matrix = txt_word_matrix.transpose()

    if max_count is not None:
        tmp = word_txt_matrix > max_count
        word_txt_matrix[tmp] = max_count

    # sum along the txt axis
    word_count_array = np.sum(word_txt_matrix, axis=1)
    # for every topic, sum the respective words counts
    topic_count_list = []
    for topic in topics.values():
        matching_words = [(w in topic) for w in words]
        matching_counts = word_count_array[matching_words]
        topic_count = np.sum(matching_counts) / len(topic)
        topic_count_list.append(topic_count)

    return topic_count_list


def unique_path(directory, name_pattern):
    counter = 0
    while True:
        counter += 1
        path = directory / name_pattern.format(counter)
        if not path.exists():
            return path