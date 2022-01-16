import pysolr

from sentence_transformers import SentenceTransformer
from search.setup_solr import constants


class SearchUtils:
    MAX_ROWS = constants.RERANK
    SOLR = pysolr.Solr(constants.SOLR_URL)
    SIMILARITY_SCORE_CUTOFF = constants.SIMILARITY_SCORE


    def __init__(self, pretrained_model_name):
        self.embedder = SentenceTransformer(pretrained_model_name)


    def get_embedding_from_sentence(self, sentence):
        return self.embedder.encode(sentence)


    def get_vector_from_embedding(self, embedding):
        return ','.join([str(emb) for emb in embedding])


    def get_vector_from_sentence(self, sentence):
        embedding = self.get_embedding_from_sentence(sentence)
        vector = self.get_vector_from_embedding(embedding)
        
        return vector


    def search_reviews(self, query, top, method):
        results = []

        if (method == "ltr"):
            results = self.search_reviews_ltr(query)
        elif (method == "bert"):
            results = self.search_reviews_bert(query)
        else:
            results = self.search_reviews_bm25(query)

        return results[:int(top)]


    def search_reviews_ltr(self, query):
        query_vector = self.get_vector_from_sentence(query)
        query_search = "{!vp f=vector vector=\"%s\"}" % (query_vector)
        fl_search = "text,score,[features]"
        rq_search = "{!ltr model=my_ranknet_model efi.text=\"%s\"}" % (query)
        
        search_results = self.SOLR.search(query_search, **{
            'rq': rq_search,
            'fl': fl_search
        }, rows=self.MAX_ROWS)
        searched_reviews = [{'rank': rank + 1, 'text': result['text'][0], 'score': result['score']} \
            for rank, result in enumerate(search_results) \
            if float(result['[features]'].split(',')[-1].split('=')[-1]) > self.SIMILARITY_SCORE_CUTOFF]

        return searched_reviews


    def search_reviews_bert(self, query):
        query_vector = self.get_vector_from_sentence(query)
        query_search = "{!vp f=vector vector=\"%s\"}" % (query_vector)
        fl_search = "text,score"

        search_results = self.SOLR.search(query_search, **{
            'fl': fl_search
        }, rows=self.MAX_ROWS)
        searched_reviews = [{'rank': rank + 1, 'text': result['text'][0], 'score': result['score']} \
            for rank, result in enumerate(search_results)]

        return searched_reviews


    def search_reviews_bm25(self, query):
        query_search = "text: (%s)" % (query)
        fl_search = "text,score"

        search_results = self.SOLR.search(query_search, **{
            'fl': fl_search
        }, rows=self.MAX_ROWS)
        searched_reviews = [{'rank': rank + 1, 'text': result['text'][0], 'score': result['score']} \
            for rank, result in enumerate(search_results)]

        return searched_reviews
