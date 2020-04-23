import logging
import sys

import discord
from discord.ext import commands

from bot import logger


class Utils(commands.Cog):
    client: commands.Bot = None

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('[cogs] [utils] Utils 모듈이 준비되었습니다.')

    # Commands
    @commands.command(name='핑', description='봇의 응답 지연 속도를 확인합니다.')
    async def ping(self, ctx: commands.Context):
        await ctx.send(f'Pong! ({round(self.client.latency * 1000)}ms)')

    @commands.command(name='정보', description='멘션한 유저의 정보를 받아옵니다.')
    async def get_user_info(self, ctx: commands.Context, member_mention: str):
        member_id: int = int(str(member_mention).translate(str.maketrans('', '', '<@!>')))
        guild: discord.Guild = ctx.guild
        member: discord.Member = guild.get_member(member_id)

        # Create an Embed which contains member's information
        info_embed: discord.Embed = discord.Embed(
            colour=discord.Colour.blue(),
            author=f'{self.client.user.name}',
            title=f'{member.display_name}',
            description=f'{member.display_name} 님의 프로필 정보입니다!',
            type='rich')
        info_embed.set_thumbnail(url=member.avatar_url)
        info_embed.add_field(name='Discord 가입 년도', value=member.created_at, inline=False)
        info_embed.add_field(name='서버 참여 날짜', value=member.joined_at, inline=True)

        await ctx.send(embed=info_embed)

    @commands.command(name='서버정보', description='현재 서버의 정보를 확인합니다.')
    async def get_server_info(self, ctx: commands.Context):
        guild: discord.Guild = ctx.guild
        # Create an Embed which contains member's information
        info_embed: discord.Embed = discord.Embed(
            colour=discord.Colour.blue(),
            author=f'{self.client.user.name}',
            title=f'{guild.name}',
            description=f'{guild.name} 서버 정보입니다!',
            type='rich')
        info_embed.set_thumbnail(url=guild.icon_url)
        info_embed.add_field(name='서버 주인', value=guild.owner.mention, inline=False)
        info_embed.add_field(name='서버 생성 날짜', value=guild.created_at, inline=True)

        await ctx.send(embed=info_embed)


def setup(client):
    logger.info('[cogs] [utils] Utils 모듈을 준비합니다.')
    client.add_cog(Utils(client))