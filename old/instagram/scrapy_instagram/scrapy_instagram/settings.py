
BOT_NAME = 'scrapy_instagram'

SPIDER_MODULES = ['scrapy_instagram.spiders']
NEWSPIDER_MODULE = 'scrapy_instagram.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Martha Garcia @martha2392'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
CLOSESPIDER_PAGECOUNT = 1000000
#LOG_LEVEL = 'DEBUG'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs

# custom martha params
DOWNLOAD_DELAY = 0.5
DOWNLOAD_TIMEOUT = 1800
#DOWNLOAD_MAXSIZE = 107374182400
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:50.0) Gecko/20100101 Firefox/50.0'

# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

ROBOTSTXT_OBEY = False


