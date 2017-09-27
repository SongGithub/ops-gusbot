"""
This module adds responses to @here and @channel
"""
import logging
import re
from slackbot.bot import listen_to, respond_to
from model.database import SESSION
from model.channel import Channel

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
    try:
        message.react('police-gus')
        message.reply(
            "Please don't use _{}_. Check out our Slacktiquete: \
            https://myob.slack.com/archives/C3F2M5NFP/p1498438403848842".format(at_symbol),
            in_thread=True
        )
    except:
        pass

@respond_to('^list$')
def list_users(msg):
    """List all users in DB"""
    LOGGER.info("LIST :: %s", msg.body['user'])
    reply = "```\n"
    reply += "{:^10} | {:^10}\n".format("Channel", "User")
    reply += "======================\n"
    for chan in Channel.query.all():
        reply += "{0.channel_name:^10} | {0.user_id:^10}\n".format(chan)
    reply += "```"
    msg.reply(reply)

@respond_to('^add.*')
@respond_to('^add (.*) to (.*)')
def add_user(msg, user=None, channel=None):
    """ Adding a new exclusion list """
    if user is None or channel is None:
        msg.reply("Usage: `add @user to #channel`")
        return

    match = parse_channel_identifier(channel)
    LOGGER.info("ADD :: %s :: %s to %s ", msg.body['user'], user, channel)
    if not match:
        LOGGER.info("ADD :: Bailing because failed to parse channel name and id: %s", channel)
        return

    LOGGER.info("ADD :: PARSED :: id: '%s', name: '%s'", match.group(1), match.group(2))

    SESSION().add(Channel(channel_id=match.group(1), channel_name=match.group(2), user_id=user))
    SESSION().commit()
    msg.reply("User {} added to {} exclusion list".format(user, channel))

def parse_channel_identifier(channel):
    """
    given a string like so "<#C04UB2PBB|ex-ea>",
    parse the ID (C04UB2PBB) and name (ex-ea) out of it
    """
    return re.search(r"<#(C[A-Z0-9]*?)\|([a-zA-Z0-9\-]*?)>", channel)

def is_allowed(user, channel):
    """
    given a user id and channel id, check if it is in the exclusion list in the DB
    """
    query = Channel.query.filter(
        Channel.channel_id == "{}".format(channel),
        Channel.user_id == "{}".format(user))
    count = query.count()
    print query

    LOGGER.info("COUNT :: %s :: %s :: %s", user, channel, count)

    if count > 0:
        return True
    return False