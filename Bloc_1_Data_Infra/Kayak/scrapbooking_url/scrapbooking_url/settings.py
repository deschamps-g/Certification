


# # Paramètres Scrapy pour le projet my_booking

# Paramètres Scrapy pour le projet my_booking

# Définissez le nom de votre projet Scrapy
BOT_NAME = "scrapbooking_url"

# Définissez les modules où se trouvent vos spiders
SPIDER_MODULES = ["scrapbooking_url.spiders"]
NEWSPIDER_MODULE = "scrapbooking_url.spiders"

# Respectez les règles de robots.txt
ROBOTSTXT_OBEY = True

# Configurez le nombre maximal de requêtes concurrentes effectuées par Scrapy
# Ajustez en fonction des capacités de votre système et de la capacité du serveur du site cible
CONCURRENT_REQUESTS = 1000

# Configurez un délai entre les requêtes pour le même site Web
# Ajustez en fonction des directives du site Web et de la vitesse de votre scraping
DOWNLOAD_DELAY = 3

# Désactivez les cookies pour éviter les problèmes liés aux sessions
COOKIES_ENABLED = False

# Activez l'extension AutoThrottle pour ajuster dynamiquement la vitesse de crawling
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1   # Délai initial de téléchargement en secondes
AUTOTHROTTLE_MAX_DELAY = 10    # Délai de téléchargement maximal en cas de latences élevées
AUTOTHROTTLE_TARGET_CONCURRENCY = 4.0  # Concurrency cible, ajustez en fonction de la capacité du serveur et de la bande passante réseau
AUTOTHROTTLE_DEBUG = False      # Désactivez le mode de débogage pour AutoThrottle

# Ajoutez un middleware pour la rotation des User-Agents
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
}

# Réglez les paramètres dont la valeur par défaut est obsolète sur une valeur résistante aux futures modifications
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.selectreactor.SelectReactor"
FEED_EXPORT_ENCODING = "utf-8"
