#! /usr/bin/env python3

"""
Bishbot - https://github.com/ldgregory/bishbot
Leif Gregory <leif@devtek.org>
space.py v0.1
Tested to Python v3.7.3

Description:
Bot commands for the Space channel

Changelog:
20200603 -  Initial code

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

import json
import requests
from discord.ext import commands


class Space(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #  Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('- Space Cog loaded')

    @commands.command(name='launches',
                    description='Show the next five launches',
                    help='Show the next five launches',
                    ignore_extra=True,
                    hidden=False,
                    enabled=True)
    async def launches(self, ctx):
        response = requests.get('https://fdo.rocketlaunch.live/json/launches/next/5')
        data = json.loads(response.text)
        launches = '**Here are the next five launches**\n\n'
        for result in data['result']:
            launches += f"- {result['quicktext']}\n"
        await ctx.channel.send(launches)


def setup(bot):
    bot.add_cog(Space(bot))
