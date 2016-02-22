# -*- coding: utf-8 -*-

# Scrapy settings for rpresults project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'rpresults'

SPIDER_MODULES = ['rpresults.spiders']
NEWSPIDER_MODULE = 'rpresults.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'rpresults (+http://www.yourdomain.com)'

USER_AGENT = "Googlebot/2.1 ( http://www.google.com/bot.html)"
ITEM_PIPELINES = {
    'rpresults.pipelines.MongodbExportPipeline': 1
}

MONGO_DBNAME = 'rpresults'

TELNETCONSOLE_PORT = None
