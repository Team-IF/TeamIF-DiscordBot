import logging
import sys

import discord
from discord.ext import commands

from bot import logger


class Help(commands.Cog):
    client: commands.Bot = None

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        logger.info('[cogs] [help] Help 모듈이 준비되었습니다.')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, e):
        logger.info(f'[cogs] [help] {self.client.command_prefix}{ctx.command} 명령어에서 오류 발생!\n{e}')

    # Commands
    @commands.command(
        name='도움말',
        description='도움말 명령어입니다.'
    )
    async def help_command(self, ctx: commands.Context, cog='all'):
        # The third parameter comes into play when
        # only one word argument has to be passed by the user

        # Prepare the help embed
        help_embed = discord.Embed(
            title='Team IF',
            description='봇 도움말',
            color=discord.Color.blue()
        )
        help_embed.set_thumbnail(url=self.client.user.avatar_url)
        help_embed.set_footer(
            text=f'Requested by {ctx.author.display_name}',
            icon_url=self.client.user.avatar_url
        )

        # Get a list of all cogs
        cogs = [c for c in self.client.cogs.keys()]

        # If cog is not specified by the user, we list all cogs and commands
        if cog == 'all':
            for cog in cogs:
                # Get a list of all commands under each cog
                cog_commands = self.client.get_cog(cog).get_commands()
                commands_list = ''
                for cmd in cog_commands:
                    commands_list += f'**{cmd.name}** : {cmd.description}\n'
                    try:
                        if type(cmd) == commands.Group:
                            for subcommand in cmd.commands:
                                commands_list += f'ㄴ {subcommand.name} : {subcommand.description}\n'
                                if len(subcommand.aliases) > 0:
                                    commands_list += f'    **동의어** : {", ".join(subcommand.aliases)}\n'
                            pass
                    except Exception as e:
                        logger.error(f'[cogs] [help] Exception occured! {e}')

                # Add the cog's details to the embed.
                help_embed.add_field(
                    name=f'**{cog}**',
                    value=commands_list,
                    inline=False
                ).add_field(
                    name='\u200b', value='\u200b', inline=False
                )
                # Also added a blank field '\u200b' is a whitespace character.
            pass

        else:
            # If the cog was specified
            lower_cogs = [c.lower() for c in cogs]

            # If the cog actually exists.
            if cog.lower() in lower_cogs:
                # Get a list of all commands in the specified cog
                commands_list = self.client.get_cog(cogs[lower_cogs.index(cog.lower())]).get_commands()

                # Add details of each command to the help text
                # Command Name
                # Description
                # Format
                for command in commands_list:
                    help_content: str = f'{command.description}\n'
                    # Also add aliases, if there are any
                    if len(command.aliases) > 0:
                        help_content += f'**동의어** : {", ".join(command.aliases)}\n'
                    else:
                        # Add a newline character to keep it pretty
                        # That IS the whole purpose of custom help
                        # help_content += '\n'
                        pass
                    if type(command) == commands.Group:
                        for subcommand in command.commands:
                            help_content += f'ㄴ **{subcommand.name}** : {subcommand.description}\n'
                            if len(subcommand.aliases) > 0:
                                 help_content += f'    **동의어** : {", ".join(subcommand.aliases)}\n'
                        pass

                    help_embed.add_field(name=f'**{command.name}**', value=f'{help_content}', inline=True)
            else:
                # Notify the user of invalid cog and finish the command
                await ctx.send('존재하지 않는 모듈입니다. `러스트봇 도움말` 명령어로 사용 가능한 모듈과 명령어를 확인해주세요!')
                return

        await ctx.send(embed=help_embed)
        return


def setup(client):
    logger.info('[cogs] [help] Help 모듈을 준비합니다.')
    client.add_cog(Help(client))