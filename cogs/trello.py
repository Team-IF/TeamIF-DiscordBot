import logging
import sys

import discord
from discord.ext import commands

from bot import logger


class Trello(commands.Cog):
    client: commands.Bot = None

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('[cogs] [trello] Trello 모듈이 준비되었습니다.')

    # Commands


def setup(client):
    logger.info('[cogs] [trello] Trello 모듈을 준비합니다.')
    client.add_cog(Trello(client))