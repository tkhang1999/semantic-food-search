import numpy as np
import pandas as pd
import pysolr
from sentence_transformers import SentenceTransformer

import constants

embedder = SentenceTransformer(constants.PRE_TRAINED_MODEL)
solr = pysolr.Solr(constants.SOLR_URL)
reviews = pd.read_csv(constants.REVIEWS_DATA_CSV)

# Number of documents to be re-ranked.
RERANK = constants.RERANK

# Build query URL.
queries = [
    {"id": 1, "text": "good chicken rice"},
    {"id": 2, "text": "not expensive food"},
    {"id": 3, "text": "not bad food"},
    {"id": 4, "text": "not good food"},
    {"id": 5, "text": "good mala"},
    {"id": 6, "text": "good food"},
]

def is_relevant(query_id, document):
    content = document['text'][0].lower()
    if (query_id == 1):
        return "chicken rice" in document['categories'][0]
    elif (query_id == 2):
        return ("cheap" in content \
            or "not expensive" in content \
            or "reasonable price" in content \
            or "average price" in content \
            or "great price" in content \
            or "acceptable price" in content) \
            and "not cheap" not in content
    elif (query_id == 3):
        return document['sentiment'][0] in ["positive", "neutral"]
    elif (query_id == 4):
        return document['sentiment'][0] in ["negative", "neutral"]
    elif (query_id == 5):
        return "mala," in document['categories'][0] \
            or ",mala" in document['categories'][0] \
            or "mala" == document['categories'][0]
    elif (query_id == 6):
        return document['sentiment'][0] == "positive"


for row in queries:
    q_id = row["id"]
    text = row["text"]

    # Encode query to BERT embedding
    query_embedding = [str(emb) for emb in embedder.encode(text)[0]]
    # Convert embedding to query vector
    query_vector = ",".join(query_embedding)

    # Get response and check for errors.
    query_search = "{!vp f=vector vector=\"%s\"}" % (query_vector)

    search_results = solr.search(query_search, **{
        "rq": "{!ltr model=my_efi_model efi.text=\"%s\"}" % (text),
        "fl": "id,score,sentiment,text,categories,[features]"
    }, rows=RERANK)

    # Extract the features.
    results_features = []
    results_targets = []
    results_ranks = []
    add_data = False

    # sorted_results = sorted(search_results, \
    #     key = lambda i: float(i['[features]'].split(',')[-1].split('=')[-1]))

    for (rank, document) in enumerate([res for res in search_results]):

        features = document["[features]"].split(",")
        feature_array = []
        for feature in features:
            feature_array.append(feature.split("=")[1])

        feature_array = np.array(feature_array, dtype = "float32")
        results_features.append(feature_array)

        doc_id = document["id"]
        # Check if document is relevant to query.
        if is_relevant(q_id, document):
            results_ranks.append(rank + 1)
            results_targets.append(1)
            add_data = True
        else:
            print(reviews.loc[reviews.id == int(doc_id), "content"].values[0])
            results_targets.append(0)

    if add_data:
        print(results_ranks)
        np.save("{0}_X.npy".format(q_id), np.array(results_features))
        np.save("{0}_y.npy".format(q_id), np.array(results_targets))
        np.save("{0}_rank.npy".format(q_id), np.array(results_ranks))
