""" This the start of the awesome GusBot """
#!/usr/bin/env python

import os
import sys
import logging
import logging.config
from slackbot import settings
from slackbot.bot import Bot
import model.database

def main():
    """ start gus bot! """
    log_config = {
        'format': '[%(asctime)s] %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': logging.DEBUG if settings.DEBUG else logging.INFO,
        'stream': sys.stdout,
    }
    logging.basicConfig(**log_config)
    logging.getLogger('requests.packages.urllib3.connectionpool').setLevel(logging.WARNING)

    # initialise the db
    model.database.init_db()

    print("printing version number")
    print(os.getenv("SLACKBOT_VERSION"))
    bot = Bot()
    bot.run()

if __name__ == '__main__':
    main()
