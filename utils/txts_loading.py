from pathlib import Path
import pandas as pd

def df_from_txts_cached(txts_dir, cache_dir):
    """Wrapper for `df_from_txts`. It loads a cached result if present,
    otherwise, it calls `df_from_txts` and caches the result.

    Args:
        cache_dir (Path object): Path to cache dir.
    """
    csv_data = cache_dir / Path('dataset.csv')
    if csv_data.exists():
        return pd.read_csv(csv_data, index_col="ID")
    else:
        df = df_from_txts(txts_dir)
        df.to_csv(csv_data)
        return df



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