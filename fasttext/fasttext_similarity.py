import fasttext

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd

model = fasttext.load_model('data/fasttext/models/full_text.bin')
x = model.get_nearest_neighbors('intelligence', k=100)
[print(j[1]) for j in x]

word_cloud = WordCloud(width=3840,height=2160, max_words=1628,relative_scaling=1,normalize_plurals=False)
weights = dict()
for word in x:
    weights[word[1]] = word[0]
print(weights.items())
word_cloud.generate_from_frequencies(weights)

plt.rcParams["figure.figsize"] = (20,14)
plt.imshow(word_cloud, interpolation='bilinear')
plt.axis("off")
plt.savefig("data/wordclouds/ex.png")
#plt.show()
