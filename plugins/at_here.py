"""
This module adds responses to @here and @channel
"""
import logging
from slackbot.bot import listen_to, respond_to


LOGGER = logging.getLogger(__name__)


@listen_to('.*(<!here>|<!channel>).*')
def at_here(message, at_symbol=None):
    """@here|@channel response"""

    channel = message.body['channel']
    user = message.body['user']

    def at_here_log(at_symbol, channel, msg, user, skip="NO_SKIP"):
        """ log line for at_here plugin """
        LOGGER.info("HERE :: [%s] %s: %s [from %s] [%s]", at_symbol, channel, msg, user, skip)

    if is_allowed(user, channel):
        at_here_log(at_symbol, channel, message.body['text'], user, "SKIP")
        return

    at_here_log(at_symbol, channel, message.body['text'], user, "NO_SKIP")
    message.react('police-gus')
    message.reply(
        "Please don't use _{}_. Check out our Slacktiquete: \
        https://myob.slack.com/archives/C3F2M5NFP/p1498438403848842".format(at_symbol),
        in_thread=True
    )


@respond_to(r'^sudo rm -rf (<@U[A-Z0-9]+>)')
def remove_from_all(msg, user):
    """
    Remove user from all whitelist rules
    Usage: sudo rm -rf @user
    """
    LOGGER.info("SUDO RM :: %s :: Removing %s from everything", msg.body['user'], user)
    rules = Channel.query.filter_by(user_id=user).all()
    if not rules:
        msg.reply("No rules for this user")
        return

    for rule in rules:
        SESSION().delete(rule)

    SESSION().commit()
    msg.reply("Deleted %d rules for %s" %(len(rules), user))

def is_allowed(user_id, channel_id):
    """
    given a user id and channel id, check if it is in the whitelist in the DB
    """
    count = Channel.query \
        .filter(Channel.channel_id == channel_id) \
        .filter(Channel.user_id == "<@"+user_id+">").count()

    LOGGER.info("COUNT :: %s :: %s :: %s", user_id, channel_id, count)

    if count > 0:
        return True
    return False
