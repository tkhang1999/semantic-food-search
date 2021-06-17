from django.apps import AppConfig
from search.utils import SearchUtils

import os

# Solr requires java to work, so we need to install java on heroku
# i.e. heroku buildpacks:add heroku/jvm

# start Solr server in background
os.system("./solr-7.7.3/bin/solr start")

class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'
    search_utils = SearchUtils('distilbert-base-nli-mean-tokens')
