"""
This module adds responses to @here and @channel
"""
import logging
from slackbot.bot import listen_to

LOGGER = logging.getLogger(__name__)

EXCLUSION_LIST = {
    #tr-platform-enable
    "C3F2M5NFP": [
        "U6DL2AHHD", # Aaron Cai
        "U0SMLP1PG", # Anthony Sceresini
        "U69G25C5Q", # Dede Lamb
        "U0QNE929J", # Gustavo Hoirisch
        "U0726J4F8", # Ian Stahnke
        "U72UJJR17", # John Contad
        "U07DUSPH6", # Kerry Wang
        "U3S3SQ96D", # Marius Nel
        "U4KRBKXJ4", # Mel Boyce
        "U0GRQSP5F", # Orlando Erazo
        "U2T5APLV7", # Paul Van de Vreede
        "U053PKM7X", # Philip Michael
        "U6DE5PBDL", # Prateek Nayak
        "U0FJ8MKAA", # Shane Corcoran
        "U5K4N2W4F", # Song Jin
        "U0ZFHNRK2", # Utkarsh Doshi
        "U665SA8SV", # Aisha Wilson
        "U053V2CBV" # Jonathan Broome
    ],
    #gus-bot-provingground
    "C745V5TD0": [
        "U5K4N2W4F" # Song Jin
    ]
}

@listen_to('.*(<!here>|<!channel>).*')
def at_here(message, at_symbol=None):
    """@here|@channel response"""

    channel = message.body['channel']
    user = message.body['user']

    def at_here_log(at_symbol, channel, msg, user, skip="NO_SKIP"):
        """ log line for at_here plugin """
        LOGGER.info("[%s] %s: %s [from %s] [%s]", at_symbol, channel, msg, user, skip)

    if message.body['user'] in EXCLUSION_LIST[channel]:
        at_here_log(at_symbol, channel, message.body['text'], user, "SKIP")
        return

    at_here_log(at_symbol, channel, message.body['text'], user, "NO_SKIP")
    message.react('police-gus')
    message.reply(
        "Please don't use _{}_. Check out our Slacktiquete: \
        https://myob.slack.com/archives/C3F2M5NFP/p1498438403848842".format(at_symbol),
        in_thread=True
    )


# @listen_to('^gus-bot configure (.*)')
# def configure(message, action=None):
#     """configure"""
#     LOGGER.info(action)
#     message.reply(message.body['text'], in_thread=True)
