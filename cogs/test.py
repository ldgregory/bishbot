#! /usr/bin/env python3

"""
Leif Gregory <leif@devtek.org>
rules.py v0.1
Tested to Python v3.7.3

Description:
Test cog for testing things out. Would suggest setting commands to hidden=True
until you move the command to a production cog.

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
import discord
from discord.ext import commands
import datetime


# Load settings from .env file
BOT_PREFIX = os.getenv('DISCORD_BOT_PREFIX')


class Test(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #  Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('- Test Cog loaded')

    @commands.command(name='file',
                    description="File persistence test",
                    help="File persistence test",
                    ignore_extra=True,
                    hidden=True,
                    enabled=True)
    async def file(self, ctx):
        with open('test.txt', 'a') as fw:
            time = datetime.datetime.now()
            data = time.strftime('%d-%b-%Y (%H:%M:%S.%f)')
            fw.write(f"{data}\n")
        await ctx.channel.send(f"Timestamp written - {data}")
        with open('test.txt', 'r') as fr:
            text = fr.read()
        await ctx.channel.send(f"\n\nContents:\n{text}")

    #  Commands
    @commands.command(name='bishop',
                    description="Bishop's Profile",
                    help="Bishop's Profile",
                    ignore_extra=True,
                    hidden=True,
                    enabled=True)
    async def bishop(self, ctx):
        embed = discord.Embed(title="Bishop",
                            color=0x0099ff,
                            url="https://devtek.org")
        embed.set_image(url="https://trucks.pcwize.com/images/gallery_monster_truckin.jpg")
        embed.set_thumbnail(url="https://2.bp.blogspot.com/-KUhSLrjqQ9A/VOIQ8eIoBWI/AAAAAAAAK7k/4ZnFWPoNSA4/s80/*'")
        embed.add_field(name="Hobbies", value="Adrenaline Rushes, coding Python, camping, off-roading, building things", inline=False)
        embed.add_field(name="Travel", value="Indonesia, Scotland, Ireland, Dominican Republic, Costa Rica, Mexico, Japan, New Zealand, Australia", inline=False)
        embed.add_field(name="Music", value="Pretty much anything, but primarily EDM", inline=False)
        embed.add_field(name="Videos", value="https://www.youtube.com/watch?v=xggSNLMuZCA\nhttps://www.youtube.com/watch?v=l7CQ3H7IMuk\nhttps://www.youtube.com/watch?v=qxM8rH6E-WE", inline=False)
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Test(bot))
