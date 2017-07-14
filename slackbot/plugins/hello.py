#coding: UTF-8
import re
from slackbot.bot import respond_to
from slackbot.bot import listen_to

@listen_to('@here')
def at_here(message):
    message.react('police-gus'),
    message.reply("Please don't use _@here_. Check out our Slacktiquete: https://myob.slack.com/archives/C3F2M5NFP/p1498438403848842", in_thread=True)

# Response type
# response trigger
# emoji
# reply or other method
# reply msg

# https://myob.slack.com/archives/C3F2M5NFP/p1498438403848842
