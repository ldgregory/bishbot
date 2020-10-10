#! /usr/bin/env python3

"""
Bishbot - https://github.com/ldgregory/bishbot
Leif Gregory <leif@devtek.org>
rules.py v0.1
Tested to Python v3.7.3

Description:
Channel rules

Changelog:
2020601 -  Initial code

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
from discord.ext import commands


# Load settings from .env file
BOT_PREFIX = os.getenv('DISCORD_BOT_PREFIX')


class Rules(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #  Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('- Rules Cog loaded')

    #  Commands
    @commands.command(name='rules',
        description="Channel Rules",
        help="Channel Rules",
        aliases=['desc', 'description'],
        ignore_extra=True,
        hidden=False,
        enabled=True)
    async def rules(self, ctx):
        if ctx.channel.name == 'bot-test':
            await ctx.channel.send(f"**{ctx.channel.name} rules:**\n"
                f"1. This is a test rule.\n"
                f"2. Bot sez I'm testing!\n")
        elif 'story-telling' in ctx.channel.name:
            await ctx.channel.send(f"**{ctx.channel.name} rules:**\n"
                f"1. One paragraph per post.\n"
                f"2. 30 minutes between posts, to let others maybe add to the story.\n"
                f"3. SFW obviously.\n"
                f"4. Don't try to derail the story. Add to it!\n")
        else:
            await ctx.channel.send(f"No rules have been defined for this channel. However, here are the general server rules:\n"
                f"1. Don't discuss actual work here, though some discussion about work is ok.\n"
                f"2. Keep it safe for work (no inappropriate language, pictures etc.)\n"
                f"3. Be civil to each other.\n"
                f"4. You're adults, you know what's illegal, immoral and inflammatory. Don't post it.")


def setup(bot):
    bot.add_cog(Rules(bot))
