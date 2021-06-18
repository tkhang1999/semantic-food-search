from django.apps import AppConfig
from search.utils import SearchUtils
from search.setup_solr import constants

import subprocess

# Solr requires java to work, so we need to install java on heroku
# i.e. heroku buildpacks:add heroku/jvm

# start Solr server in background
subprocess.Popen(['./solr-6.6.0/bin/solr', 'start'])

class SearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'search'
    search_utils = SearchUtils(constants.PRE_TRAINED_MODEL)
