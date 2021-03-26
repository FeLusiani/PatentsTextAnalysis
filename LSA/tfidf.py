from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import save_npz, load_npz
from pathlib import Path
import pickle
import logging

# from nonnegfac.nmf import NMF
from utils import df_from_txts

# df = df["Text"].to_numpy()

def tfidf_compute_cached(*args, cache_dir, **kwargs):
    """Wrapper for `tfidf_compute`. It loads a cached result if present,
    otherwise, it calls `tfidf_compute` and caches the result.

    Args:
        cache_dir (Path object): Path to cache dir.
    """
    tfidf_dir = cache_dir / Path('TFIDF')
    if tfidf_dir.exists():
        return tfidf_load(tfidf_dir)
    else:
        word_document_matrix, matrix_words = tfidf_compute(*args, **kwargs)
        tfidf_save(tfidf_dir, word_document_matrix,matrix_words)
        return word_document_matrix, matrix_words


def tfidf_compute(corpus, vocab_size=1000, stop_words: list = None):
    """Compute tfidf on `corpus` text array.
    Returns a tuple made of word-document matrix, and a list of
    the matrix row indexes (words).
    It uses `TfidfVectorizer` from `sklearn.feature_extraction.text`.

    Args:
        corpus (str array): array of documents
        vocab_size (int, optional): Number of words to extract. Defaults to 1000.
        stop_words (list, optional): Stop-words list for tfidf_vectorizer. Defaults to None.

    Returns:
        (tuple): word_document_matrix, matrix_words
    """
    logging.info(f"Computing TFIDF...")
    # stop_words = ["may", "said", "the", "one"]
    tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words, max_features=vocab_size)
    document_term_matrix = tfidf_vectorizer.fit_transform(corpus)
    tfidf_words = tfidf_vectorizer.get_feature_names()
    return document_term_matrix.transpose(), tfidf_words


def tfidf_save(tfidf_dir:Path, tfidf_matrix, tfidf_words:list):
    """Save output from `tfidf_compute`.

    Args:
        tfidf_dir (Path): tfidf cache directory
        tfidf_matrix (sparse matrix): tfidf matrix
        tfidf_words (list): tfidf matrix row indexes
    """
    tfidf_matrix_f = tfidf_dir / Path("tfidf_matrix.npz")
    tfidf_words_f = tfidf_dir / Path("tfidf_words.pkl")
    logging.info(f"Saving TFIDF output in \n {tfidf_dir}")
    tfidf_dir.mkdir(exist_ok=True)
    save_npz(tfidf_matrix_f, tfidf_matrix, compressed=True)
    f = open(tfidf_words_f, "wb")
    pickle.dump(tfidf_words, f)
    f.close()


def tfidf_load(tfidf_dir:Path):
    """Loads cached output computed with `tfidf_compute` and saved with `tfidf_save`.

    Args:
        tfidf_dir (Path): tfidf cache directory
    
    Returns:
        (tuple): word_document_matrix, matrix_words
    """
    print(f"Loading cached TFIDF output from \n {tfidf_dir}")
    tfidf_matrix_f = tfidf_dir / Path("tfidf_matrix.npz")
    tfidf_words_f = tfidf_dir / Path("tfidf_words.pkl")
    word_document_matrix = load_npz(tfidf_matrix_f)
    f = open(tfidf_words_f, "rb")
    tfidf_words = pickle.load(f)
    f.close()
    return word_document_matrix, tfidf_words
