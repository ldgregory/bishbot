#! /usr/bin/env python3

"""
Leif Gregory <leif@devtek.org>
bishbot.py v0.8
Tested to Python v3.7.3

Description:
Discord Bot

Changelog:
20200728 -  Cleanup and testing for commiting to git
20200522 -  Significant rewrite to use COGS
20200521 -  Better error handling
20200520 -  Case insensitive bot commands, tips, DM nickname change
20200519 -  Total code refactor
            Moved to external text files to clean up code
            Got rid of aiohttp library for images
            Beefed up $server information
20200518 -  Added 8-Ball, Insults, PEP-8 compliance, Bot status message
20200517 -  Adding various commands
20200516 -  Initial code

Todo:
Move load, unload and reload commands to cogs/utility.py

Dependencies:
python3 -m pip install -U discord.py
python3 -m pip install -U python-dotenv

Copyright 2020 Leif Gregory

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import os
import discord

from discord.ext import commands, tasks
from dotenv import load_dotenv
from itertools import cycle


class TextColor:
    BLOGR = str('\033[7;32m')
    BLUE = str('\033[1;34m')
    GREEN = str('\033[1;32m')
    PURPLE = str('\033[1;35m')
    RED = str('\033[1;31m')
    RESET = str('\033[0m')
    YELLOW = str('\033[1;33m')


def random_responses(file):
    """
    Loads an array of responses from a txt file.
    This function does not strip \n intentionally.

    Arguments:
        file {text} -- possible responses, one per line

    Returns:
        array -- array of possible responses
    """

    with open(file, 'r') as fh:
        lines = []
        for line in fh:
            lines.append(line)

    return lines


def read_file(file):
    """
    Loads a text file to output informational text.
    This function does not strip \n intentionally.

    Arguments:
        file {text} -- complete text of file

    Returns:
        str -- complete text of file
    """

    with open(file, 'r') as fh:
        text = fh.read()

    return text


# Load responses
change_nickname_text = read_file('txt/bb_change_nickname.txt')
change_bot_status_text = random_responses('txt/bb_bot_status.txt')


def main():
    # Load settings from .env file
    load_dotenv()
    BOT_PREFIX = os.getenv('DISCORD_BOT_PREFIX')
    GUILD = os.getenv('DISCORD_GUILD')
    TOKEN = os.getenv('DISCORD_TOKEN')
    ERROR_LOG = os.getenv('DISCORD_ERROR_LOG')

    #  Instantiate bot and set prefix to listen for
    bot = commands.Bot(command_prefix=BOT_PREFIX, case_insensitive=True)
    bot_status = cycle(change_bot_status_text)

#  Cogs management
    @bot.command(name='load',
                description='Load a cog',
                help='Load a cog',
                ignore_extra=True,
                hidden=True,
                enabled=True)
    async def load(ctx, extension):
        bot.load_extension(f"cogs.{extension.lower()}")
        await ctx.channel.send(f"Cog {extension.lower()} loaded.")

    @bot.command(name='reload',
                description='Reload a cog',
                help='Reload a cog',
                ignore_extra=True,
                hidden=True,
                enabled=True)
    async def _reload(ctx, extension):
        bot.unload_extension(f"cogs.{extension.lower()}")
        bot.load_extension(f"cogs.{extension.lower()}")
        await ctx.channel.send(f"Cog {extension.lower()} reloaded.")

    @bot.command(name='unload',
                description='Unload a cog',
                help='Unload a cog',
                ignore_extra=True,
                hidden=True,
                enabled=True)
    async def unload(ctx, extension):
        bot.unload_extension(f"cogs.{extension.lower()}")
        await ctx.channel.send(f"Cog {extension.lower()} unloaded.")

    #  Do initial load of cogs on bot start in cogs folder
    #  Either rename unwanted cogs to different extension or move them out of
    #  the cogs folder.
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f"cogs.{filename[:-3]}")


#  Bot Events ------------------------------------------------------------------
    #  Send a DM to new members about changing their nickname
    @bot.event
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(change_nickname_text)

    # Send a message to general that someone important showed up
    @bot.event
    async def on_member_update(before, after):
        if str(after.status) == "online" and (str(after.id) == "DISCORD_ID" or str(after.id) == "DISCORD_ID"):
            channel = discord.utils.get(after.guild.channels, name='general')
            await channel.send(f"Quick!!! Look busy! One of the big bosses are online! ({after.name})")

#  Error handling logged to ERROR_LOG file
    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.channel.send(f"Beep, boop! Does not compute. Maybe try {BOT_PREFIX}help.")
        elif isinstance(error, commands.DisabledCommand):
            await ctx.channel.send(f"Beep, boop! Sorry, that command is currently disabled.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send(f"Beep, boop! Err, something's missing here. Try {BOT_PREFIX}help.")
        elif isinstance(error, commands.TooManyArguments):
            await ctx.channel.send(f"Beep, boop! Buffer overflow! Too many arguments.")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.send(f"Beep, boop! Command is smoking hot! Give it a few minutes to cool down.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.channel.send(f"Beep, boop! Denied! You don't have access!.")
        with open(ERROR_LOG, 'a') as fh:
            fh.write(f"Unhandled message: {error}\n")

# Changes the bot status to random statuses pulled from txt/bb_bot_status.txt
    @tasks.loop(seconds=60)
    async def change_bot_status():
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(bot_status)))

#  Information about our bot and its status when run
    @bot.event
    async def on_ready():
        change_bot_status.start()
        guild = discord.utils.get(bot.guilds, name=GUILD)
        print(f"{TextColor.BLUE}{bot.user} (id: {bot.user.id}) is connected to {guild.name} (id: {guild.id}){TextColor.RESET}")
        print(f"{TextColor.GREEN}{bot.user.name} is ready!{TextColor.RESET}")

    bot.run(TOKEN)


if __name__ == '__main__':
    main()
