import logging
import sys

import discord
from discord.ext import commands

from bot import save_datas, logger


class Management(commands.Cog):
    client: commands.Bot = None

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('[cogs] [management] management 모듈이 준비되었습니다.')

    # Commands
    @commands.has_guild_permissions(administrator=True)
    @commands.command(name='메세지청소')
    async def purge_cmd(self, ctx: commands.Context, amount=5):
        deleted: list = await ctx.channel.purge(limit=amount)
        await ctx.send(f'{len(deleted)} 개의 메세지를 삭제했습니다!')

    @commands.has_role(item='개발진')
    @commands.command(name='설정저장')
    async def save_datas_cmd(self, ctx: commands.Context):
        await ctx.send('설정파일을 저장합니다...')
        result, error = save_datas()
        await ctx.send(f'> 결과 : {result}')
        if error is not None:
            await ctx.send(f'> 오류 : {type(error)} : {error}')

    @commands.has_role(item='개발진')
    @commands.cooldown(rate=1, per=60)
    @commands.is_owner()
    @commands.command(name="종료")
    async def stop(self, ctx: discord.ext.commands.Context):
        self.client.do_reboot = False
        logger.info(f'{ctx.author} 님이 봇을 종료시켰습니다.')
        await ctx.send('봇을 종료합니다...')
        await self.client.close()

    @commands.cooldown(rate=1, per=60)
    @commands.has_role(item='개발진')
    @commands.command(name="재시작")
    async def restart(self, ctx: discord.ext.commands.Context):
        self.client.do_reboot = True
        logger.info(f'{ctx.author} 님이 봇을 재시작시켰습니다.')
        await ctx.send('봇을 재시작합니다...')
        await self.client.close()


def setup(client):
    logger.info('[cogs] [management] management 모듈을 준비합니다.')
    client.add_cog(Management(client))
