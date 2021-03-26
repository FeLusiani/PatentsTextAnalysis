from sklearn.decomposition import non_negative_factorization
from sklearn.utils.extmath import randomized_svd
import logging
from pathlib import Path
import numpy as np

def lsa_compute_cached(*args, cache_dir, **kwargs):
    """Wrapper for `lsa_compute`. It loads a cached result if present,
    otherwise, it calls `lsa_compute` and caches the result.

    Args:
        cache_dir (Path object): Path to cache dir.
    """
    lsa_dir = cache_dir / Path('LSA_' + kwargs['method'])
    if lsa_dir.exists():
        return lsa_load(lsa_dir)
    else:
        word_topic_matrix, topic_doc_matrix = lsa_compute(*args, **kwargs)
        lsa_save(lsa_dir, word_topic_matrix, topic_doc_matrix)
        return word_topic_matrix, topic_doc_matrix


def lsa_compute(word_doc_matrix, n_topics: int, method='SVD', max_nmf_iter=10):
    """
    Computes lsa on word_doc_matrix, using factorization functions from `sklearn`.
    If `method` is "SVD" (default), it will use `randomized_svd`.
    If `method` is "NMF", it will use `non_negative_factorization`.

    Args:
        word_doc_matrix (matrix): matrix to factorize
        n_topics (int): number of "topics" to extract
        method (str): factorization method
        max_nmf_iter (int, optional): Sets the max number of iterations
            when calling `non_negative_factorization`. Default is 10.

    Returns:
        tuple of word_topic_matrix, topic_doc_matrix
    """

    logging.info(f"Computing LSA using {method} method...")

    if method == "SVD":
        U, _, VT = randomized_svd(word_doc_matrix, n_topics)
        return U, VT
    elif method == "NMF":
        W, H, _ = non_negative_factorization(
            word_doc_matrix,
            n_components=n_topics,
            max_iter=max_nmf_iter,
            random_state=0,
        )
        return W, H
    else:
        raise ValueError(f"ERROR: invalid value for method argument")


def lsa_save(lsa_dir: Path, word_topic_matrix, topic_doc_matrix):
    """Save output computed by `lsa_compute` with method `method`.

    Args:
        lsa_dir (Path): cache directory
        word_topic_matrix (matrix): lsa topics as words-embedding
        topic_doc_matrix (matrix): lsa topics as documents-embedding
    """
    logging.info(f"Saving LSA output to {lsa_dir}")
    lsa_dir.mkdir(
        parents=True,
        exist_ok=True,
    )
    WTM_file = lsa_dir / Path("word_topic_matrix.npy")
    TDM_file = lsa_dir / Path("topic_doc_matrix.npy")
    np.save(WTM_file, word_topic_matrix)
    np.save(TDM_file, topic_doc_matrix)


def lsa_load(lsa_dir: Path):
    """Loads cached output computed with `lsa_compute`,
    and then saved with `lsa_save`.

    Args:
        lsa_dir (Path): cache directory

    Returns:
        (tuple): word_document_matrix, matrix_words
    """
    print(f"Loading cached LSA output from \n {lsa_dir}")
    WTM_file = lsa_dir / Path("word_topic_matrix.npy")
    TDM_file = lsa_dir / Path("topic_doc_matrix.npy")
    word_topic_matrix = np.load(WTM_file)
    topic_doc_matrix = np.load(TDM_file)
    return word_topic_matrix, topic_doc_matrix