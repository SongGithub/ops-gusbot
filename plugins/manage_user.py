"""
This module manages users
"""
import logging
from slackbot.bot import respond_to
from model.database import SESSION
from model.channel import Channel


LOGGER = logging.getLogger(__name__)


@respond_to('^list$')
def list_users(msg):
    """
    List all whitelist rules
    Usage: `list`
    """
    LOGGER.info("LIST :: %s", msg.body['user'])
    reply = "```\n"
    for chan in Channel.query.order_by(Channel.user_id.asc()).all():
        reply += "{0.user_id:^20} | {0.channel_name:^20}\n".format(chan)
    reply += "```"
    msg.reply(reply)


@respond_to(r'^add (<@U[A-Z0-9]+>) to <#(C[A-Z0-9]*?)\|([a-zA-Z0-9\-]*?)>')
def add_user(msg, user, channel_id, channel_name):
    """
    Add a user to a channel whitelist
    Usage: `add @user to #channel`
    """
    LOGGER.info("ADD :: %s :: %s to %s ", msg.body['user'], user, channel_name)
    records = Channel.query.filter_by(channel_id=channel_id, user_id=user).all()
    if records:
        msg.reply("Rule already exists.")
        return
    SESSION().add(Channel(channel_id=channel_id, channel_name=channel_name, user_id=user))
    SESSION().commit()
    msg.reply("User {} added to {} whitelist".format(user, channel_name))


@respond_to(r'^remove (<@U[A-Z0-9]+>) from <#(C[A-Z0-9]*?)\|([a-zA-Z0-9\-]*?)>')
def remove_user(msg, user, channel_id, channel_name):
    """
    Remove a user from a channel whitelist
    Usage: `remove @user from #channel`
    """
    LOGGER.info("REMOVE :: %s :: %s from %s ", msg.body['user'], user, channel_name)
    record = Channel.query.filter_by(channel_id=channel_id, user_id=user).first()
    if not record:
        msg.reply("Could not find whitelist rule.")
        return
    SESSION().delete(record)
    SESSION().commit()
    msg.reply("User {} deleted from {} whitelist.".format(user, channel_name))


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
