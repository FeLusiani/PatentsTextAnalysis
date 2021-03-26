import numpy as np
import matplotlib.pyplot as plt



def get_topic_words(word_topic_matrix, words, N=3):
    """
    Returns the top N words of each topic.
    """
    words = np.array(words)
    n_topics = word_topic_matrix.shape[1]
    topic_top_words = []
    # print('Printing top-{N} words for each topic:')
    for topic in range(n_topics):
        top_words_indexes = word_topic_matrix[:,topic].argsort(axis=0)[-N:]
        top_words = words[top_words_indexes]
        topic_top_words.append(top_words)
        # print(f"Topic {topic}: {' '.join(top_words)}")
    return topic_top_words


def get_topic_counts(topic_doc_matrix):
    """
    Assigns each document to a topic based on the `topic_doc_matrix`,
    and returns the total number of documents assigned to each topic.

    To assign a document to a topic, it searches for the greater component
    in the topic-embedding of the document.  
    """
    n_topics = topic_doc_matrix.shape[0]
    document_topic = topic_doc_matrix.argmax(axis=0)
    document_topic = list(document_topic)
    # count the number of documents belonging to each topic
    topic_count = []
    for topic in range(n_topics):
        n_assigned = document_topic.count(topic)
        topic_count.append(n_assigned)
    return topic_count

def plot_lsa(topic_words, topic_counts, N=-1):
    """Plot the number of documents assigned to each topic.
    It also displays the top words of each topic.

    Args:
        topic_words (list): top words for each topic
        topic_counts (list): number of documents for each topic
        N (int): If set, shows only the top `N` topics.
    """
    topic_counts = np.array(topic_counts)
    topics_order = np.argsort(-topic_counts)
    if N>0: topics_order = topics_order[:N]

    n_topics = len(topics_order)
    labels = [f'Topic {i}: \n' + '\n'.join(topic_words[i]) for i in topics_order]

    _, ax = plt.subplots(figsize=(16,8))
    ax.bar(range(n_topics), [topic_counts[i] for i in topics_order])
    ax.set_xticks(range(n_topics))
    ax.set_xticklabels(labels)
    ax.set_ylabel('Number of patents')
    ax.set_title('LSA topic counts')
    plt.show()