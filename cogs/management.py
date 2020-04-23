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
    @commands.command(name='메세지청소', description='메세지를 주어진 개수만큼 삭제합니다.')
    async def purge_cmd(self, ctx: commands.Context, amount=5):
        deleted: list = await ctx.channel.purge(limit=amount+1)
        await ctx.send(f'{len(deleted)} 개의 메세지를 삭제했습니다!')

    @commands.has_guild_permissions(administrator=True)
    @commands.command(name='투표',
                    description='투표를 생성합니다. 사용 양식은 아래와 같습니다 :\n'
                                '__러스트봇 관리 투표 {제목}/[{선택1}/{선택2}/.../{선택9}]\n__'
                                '제목은 반드시 입력하셔야 하며, 선택지는 두개 이상 9개 이하로 입력하셔야 합니다.')
    async def create_vote(self, ctx: commands.Context, vote_content: str):
        num_unicode_emoji: list = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣']  # 1~9

        # Process vote_content to title(str), choices(list[str])
        vote_datas: list = vote_content.translate(str.maketrans('', '', '{}')).split('/')
        title: str = vote_datas.pop(0)  # First content from vote_content must be the title
        logger.info(f'title = {title}')
        logger.info(f'vote_datas = {vote_datas}')
        choices = vote_datas
        del vote_datas

        choices_count: int = len(choices)

        # Check if the command is used properly
        # If vote has only one choice or no choice:
        if 2 > choices_count or choices_count > 9:
            await ctx.send(f'투표는 2개 이상 9개 이하의 선택지로 구성되어야 합니다!')
            return
        # If vote does not have a title:
        if title == '':
            await ctx.send(f'투표 제목 없이는 투표를 진행할 수 없습니다.')
            return

        # Create an Embed which contains informations of this vote:
        vote_embed = discord.Embed(title=f"[투표] {title}", colour=discord.Colour.dark_red())

        # Loops for add choices field in vote_embed:
        for num in range(choices_count):
            vote_embed.add_field(name=num_unicode_emoji[num], value=choices[num], inline=True)

        vote_embed.add_field(name='게시 일자', value=ctx.message.created_at, inline=False)
        vote_embed.add_field(name='주의사항', value='현재 봇은 투표 결과를 자동으로 집계해주진 않습니다.\n'
                                                '각 문항별 득표수는 해당 문항의 반응 개수 - 1(봇이 남긴 반응)입니다.', inline=False)

        vote_msg: discord.Message = await ctx.send(embed=vote_embed)

        # Loops for add number reaction in vote_msg:
        for num in range(choices_count):
            await vote_msg.add_reaction(num_unicode_emoji[num])

    @commands.has_role(item='개발진')
    @commands.command(name='설정저장', description='봇의 설정을 저장합니다.')
    async def save_datas_cmd(self, ctx: commands.Context):
        logger.info(f'{ctx.author} 님이 설정을 저장했습니다.')
        await ctx.send('설정파일을 저장합니다...')
        result, error = save_datas()
        await ctx.send(f'> 결과 : {result}')
        if error is not None:
            await ctx.send(f'> 오류 : {type(error)} : {error}')

    @commands.has_role(item='개발진')
    @commands.cooldown(rate=1, per=60)
    @commands.command(name="종료", description='봇을 종료시킵니다.')
    async def stop(self, ctx: discord.ext.commands.Context):
        self.client.do_reboot = False
        logger.info(f'{ctx.author} 님이 봇을 종료시켰습니다.')
        await ctx.send('봇을 종료합니다...')
        await self.client.close()

    @commands.cooldown(rate=1, per=60)
    @commands.has_role(item='개발진')
    @commands.command(name="재시작", description='봇을 재시작합니다.')
    async def restart(self, ctx: discord.ext.commands.Context):
        self.client.do_reboot = True
        logger.info(f'{ctx.author} 님이 봇을 재시작시켰습니다.')
        await ctx.send('봇을 재시작합니다...')
        await self.client.close()


def setup(client):
    logger.info('[cogs] [management] management 모듈을 준비합니다.')
    client.add_cog(Management(client))
