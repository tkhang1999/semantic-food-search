from django.apps import AppConfig
from search.utils import SearchUtils, start_solr_server
from search.setup_solr import constants


class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'
    search_utils = SearchUtils(constants.PRE_TRAINED_MODEL)

    def ready(self):
        start_solr_server()
