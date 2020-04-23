# -*- coding:utf-8 -*-
import logging
import sys
import os
import traceback

import discord
from discord.ext import commands

# 로깅 설정
logging.getLogger("discord.gateway").setLevel(logging.WARNING)
logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(name)s: %(message)s'))
logger.addHandler(handler)

# 봇 설정 변수들.
token: str = ''


class IFBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        self.dev_ids: list = [280855156608860160]
        self.do_reboot: bool = False
        super.__init__(*args, **kwargs)


desc = 'Team IF 서버관리 및 개발 자동화용 디스코드 봇입니다.'
bot = commands.Bot(command_prefix='!', description=desc)  # 봇 변수
bot.do_reboot = False  # 봇 재시작 명령어 체크용 flag

"""
[ Cogs Management ]
Using discord.ext.commands.Cog, this bot manages several function per extension.
"""


@commands.has_role(item='개발진')
@bot.group(name="모듈", invoke_without_command=True)
async def manage_module(ctx: commands.Context):
    msg = '>>> **현재 불러와진 모듈**'
    for module in bot.extensions:
        msg += f'\n \* {str(module).replace("cogs.", "")}'

    msg += '\n\n사용법: `모듈 (로드/언로드/리로드) [모듈이름]`'
    await ctx.send(msg)


@commands.has_role(item='개발진')
@manage_module.command(name="로드")
async def cmd_cog_load(ctx: commands.Context, extension: str):
    try:
        bot.load_extension(f'cogs.{extension}')
    except commands.errors.ExtensionNotFound:
        return await ctx.send('해당 모듈을 찾을 수 없습니다.')
    except commands.errors.ExtensionAlreadyLoaded:
        return await ctx.send('해당 모듈은 이미 불러와졌습니다.')
    except commands.errors.NoEntryPointError:
        return await ctx.send('해당 모듈에 setup() 함수가 없습니다."')
    except commands.errors.ExtensionFailed:
        return await ctx.send('해당 모듈의 setup() 실행에 실패했습니다.')
    except Exception as e:
        logger.exception(f'Error while load cog {extension}')
        return await ctx.send('모듈에 문제가 발생했습니다!'
                              + f'\n > Exception Type : {type(e)}'
                              + f'\n > Exception Content : {e}')
    else:
        return await ctx.send(f'> {extension} 모듈을 로드했습니다.')


@commands.has_role(item='개발진')
@manage_module.command(name="언로드")
async def cmd_cog_unload(ctx: commands.Context, extension: str):
    try:
        bot.unload_extension(f'cogs.{extension}')
    except commands.errors.ExtensionNotLoaded:
        return await ctx.send('해당 모듈이 로드되지 않았습니다.')
    except Exception as e:
        logger.exception(f'Error while load cog {extension}')
        return await ctx.send('모듈에 문제가 발생했습니다!'
                              + f'\n > Exception Type : {type(e)}'
                              + f'\n > Exception Content : {e}')
    else:
        return await ctx.send(f'> {extension} 모듈을 언로드했습니다.')


@commands.has_role(item='개발진')
@manage_module.command(name="리로드")
async def cmd_cog_reload(ctx: commands.Context, extension: str):
    try:
        bot.reload_extension(f'cogs.{extension}')
    except commands.errors.ExtensionNotLoaded:
        return await ctx.send('해당 모듈이 로드되지 않았습니다.')
    except commands.errors.ExtensionNotFound:
        return await ctx.send('해당 모듈을 찾을 수 없습니다.')
    except commands.errors.NoEntryPointError:
        return await ctx.send('해당 모듈에 setup() 함수가 없습니다.')
    except commands.errors.ExtensionFailed:
        return await ctx.send('해당 모듈의 setup() 실행에 실패했습니다.')
    except Exception as e:
        logger.exception(f'Error while load cog {extension}')
        return await ctx.send('모듈에 문제가 발생했습니다!'
                              + f'\n > Exception Type : {type(e)}'
                              + f'\n > Exception Content : {e}')
    else:
        return await ctx.send(f'> {extension} 모듈을 리로드했습니다.')


def init():
    """
    initialize several configs, cogs of the bot.
    :return: None
    """

    # Collect token
    global token
    try:
        logger.info('[init] > config.txt를 불러옵니다.')
        with open(file='config.txt', mode='rt', encoding='utf-8') as bot_config_file:
            # Loaded 'config.txt', load token from the file.
            token = bot_config_file.read().replace('token=', '')
            logger.info(f'[init] > config.txt 를 성공적으로 불러왔습니다. > token : {token}')
            if token == '':
                logger.info('[init] > config.txt를 불러왔으나, token이 비어있네요 :(')
                token = input('[init] > discord application의 bot token을 입력해 주세요! : ')
                logger.info(f'token = {token}')
    except FileNotFoundError as e:
        # Since 'config.txt' file not exists, create a new file and write a token in it.
        logger.info(f'[init] > Exception Type : {type(e)}')
        logger.info(f'[init] > Exception Value : {e}')
        logger.info('[init] > config.txt 가 존재하지 않습니다! 새로 생성합니다...')
        token = input('[init] > discord application의 bot token을 입력해 주세요! : ')
        with open(mode='xt', file='config.txt', encoding='utf-8') as bot_config_file:
            bot_config_file.write(f'token={token}')

    # Load Cogs(Extensions)
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            extension = filename[0:-3]
            logger.info(f'filename[0:3] = {extension}')
            bot.load_extension(f'cogs.{extension}')


def save_datas():
    try:
        # Save 'config.txt'
        logger.info('[save_datas] > config.txt를 저장합니다...')
        with open(file='config.txt', mode='wt', encoding='utf-8') as bot_config_file:
            bot_config_file.write(f'token={token}')
    except Exception as e:
        logger.info('[save_datas] > 오류가 발생했습니다!')
        logger.info(f'[save_datas] > Exception Type : {type(e)}')
        logger.info(f'[save_datas] > Exception Value : {e}')

        result = '오류 발생!'
        error = e
    else:
        logger.info('[save_datas] > config.txt를 저장했습니다!')
        result = '저장 성공!'
        error = None
    finally:
        return result, error


"""
[ Discord.py Events ]
on_ready(): 
"""


@bot.event
async def on_ready():
    logger.info(f'discord.py version : {discord.__version__} ({discord.version_info})')
    logger.info(f'봇이 다음 옵션으로 실행되었습니다. :\ncommand_prefix : {bot.command_prefix}')
    logger.info(f'현재 로드된 모듈 목록입니다 :\nextensions: {bot.extensions}')


@bot.event
async def on_command_error(ctx: commands.Context, e: Exception):
    await ctx.send(f'> **{ctx.command}** 명령어에서 오류가 발생했습니다!\n {e.with_traceback(e.__traceback__)}')


init()
bot.run(token)
result, error = save_datas()
print(f'save_datas() result = {result}')
if error is not None:
    print(f'save_datas() error type = {type(result)}')
    print(f'save_datas() error content = {str(result)}')

# if reboot mode on, run reboot code
print(f' Is bot need to be rebooted? : {bot.is_closed() and bot.do_reboot}')
if bot.is_closed() and bot.do_reboot:
    print('[bot.py] > 봇 재시작 명령이 들어와 봇을 재시작합니다 :')
    excutable = sys.executable
    args = sys.argv[:]
    args.insert(0, excutable)
    os.execv(sys.executable, args)
