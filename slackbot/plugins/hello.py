#coding: UTF-8
"""
This module contains all the instructions for the replies Gus Bot will have
"""
from slackbot.bot import listen_to

@listen_to('<!here>')
def at_here(message):
    """
    at_here responds to any @here in slack
    """
    message.react('police-gus')
    message.reply(
        "Please don't use _@here_. Check out our Slacktiquete: \
        https://myob.slack.com/archives/C3F2M5NFP/p1498438403848842",
        in_thread=True
    )

@listen_to('<!channel>')
def at_channel(message):
    """
    at_channel responds to any @channel in slack
    """
    message.react('police-gus')
    message.reply(
        "Please don't use _@channel_. Check out our Slacktiquete: \
        https://myob.slack.com/archives/C3F2M5NFP/p1498438403848842",
        in_thread=True
    )
