#coding: UTF-8
import re
from slackbot.bot import respond_to
from slackbot.bot import listen_to


@listen_to('<!here>')
def at_here_II(message):
    message.react('police-gus'),
    message.reply("Please don't use _@here_. Check out our Slacktiquete: \
        https://myob.slack.com/archives/C3F2M5NFP/p1498438403848842",
        in_thread=True)


@listen_to('<!channel>')
def at_channel(message):
    message.react('police-gus'),
    message.reply("Please don't use _@channel_. Check out our Slacktiquete: \
        https://myob.slack.com/archives/C3F2M5NFP/p1498438403848842",
        in_thread=True)
