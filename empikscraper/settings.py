BOT_NAME = 'empikscraper'
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'Empik'


SPIDER_MODULES = ['empikscraper.spiders']
NEWSPIDER_MODULE = 'empikscraper.spiders'

#USER_AGENT = 'empikscraper (+http://www.yourdomain.com)'

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    'empikscraper.pipelines.DuplicatesPipeline': 300,
    'empikscraper.pipelines.MongoPipeline': 800,
}

#DOWNLOAD_DELAY = 3
#COOKIES_ENABLED = False
#TELNETCONSOLE_ENABLED = False

#AUTOTHROTTLE_ENABLED = True
#AUTOTHROTTLE_START_DELAY = 5
#AUTOTHROTTLE_MAX_DELAY = 60
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
#AUTOTHROTTLE_DEBUG = False
