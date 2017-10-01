"""
This module adds responses to general bot management tasks.
"""
import os
import logging
from slackbot.bot import respond_to


LOGGER = logging.getLogger(__name__)


@respond_to('^version$')
def check_version(msg):
    """
    check current running version
    Usage: `version`
    """
    user = msg.body['user']
    build = os.getenv("SLACKBOT_VERSION")
    reply = "Current bot build is: {}".format(build)
    LOGGER.info("user {} checked version of the bot".format(user)
        + "and my reply was: "
        + reply)

    msg.reply(reply,in_thread=False)
