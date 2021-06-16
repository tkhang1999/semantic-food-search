import pandas as pd
import pysolr
from sentence_transformers import SentenceTransformer
import tqdm

import constants

# Read reviews data
reviews = pd.read_csv(constants.REVIEWS_DATA_CSV)

# Encode reviews to BERT embeddings
corpus = reviews['content']
embedder = SentenceTransformer(constants.PRE_TRAINED_MODEL)

print("Encoding reviews to BERT embeddings:")
corpus_embeddings = embedder.encode(corpus, show_progress_bar=True)

# Convert embedding to vector format
vectors = []
for embedding in tqdm.tqdm(corpus_embeddings, desc="Converting embedding to vector format"):
    vector = []
    for i in range(len(embedding)):
        vector.append(str(i) + "|" + str(embedding[i]))
    vectors.append(vector)

vectors = [' '.join(vector) for vector in vectors]

# Data to be indexed to Solr
data = [{"id": rid, "sentiment": sen, "text": rev, "categories": cat, "vector": vec} for rid, sen, rev, cat, vec in \
    zip(reviews['id'], reviews['content_type'], reviews['content'], reviews['categories'], vectors)]

# Index data and add to Solr with core 'bert'
solr = pysolr.Solr(constants.SOLR_URL, always_commit=True)
print("Add data to Solr:")
print(solr.add(data))
