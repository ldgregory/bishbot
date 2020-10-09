#! /usr/bin/env python3

"""
Bishbot - https://github.com/ldgregory/bishbot
Leif Gregory <leif@devtek.org>
fun.py v0.1
Tested to Python v3.7.3

Description:
Fun commands for everyone

Changelog:
20200522 -  Initial code

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
import os
import random
import requests
from discord.ext import commands


def random_responses(file):
    '''
    Loads an array of responses from a txt file.
    Text files are in the format of one response per line.
    This function does not strip \n intentionally.
    '''
    with open(file, 'r') as fh:
        lines = []
        for line in fh:
            lines.append(line)

    return lines


def read_file(file):
    '''
    Loads a text file to output informational text.
    This function does not strip \n intentionally.
    '''
    with open(file, 'r') as fh:
        text = fh.read()

    return text


# Load settings from .env file
BOT_PREFIX = os.getenv('DISCORD_BOT_PREFIX')

# Load responses to random responders.
# A note on paths, as this is a COG, it paths from the calling bot script
eight_ball_responses = random_responses('txt/bb_8ball.txt')
insult_responses = random_responses('txt/bb_insults.txt')

# Load text responses
# A note on paths, as this is a COG, it paths from the calling bot script
bishbot_text = read_file('txt/bb_bishbot.txt')

# Onwer name for 8ball easter egg
owner_name = 'Bishop'


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #  Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('- Fun Cog loaded')

    #  Commands
    @commands.command(name='8ball',
        description="Answers a yes/no question.",
        help="Magic 8-ball, ask it a yes/no question.",
        aliases=['eight_ball', 'eightball', '8-ball'],
        ignore_extra=True,
        hidden=False,
        enabled=True)
    async def eight_ball(self, ctx, *, phrase=None):
        if f"is {owner_name.lower()} cool" in phrase.lower():
            await ctx.channel.send(f"{owner_name} is the best! {owner_name} is Awesome! {owner_name} rocks the world! Everybody loves {owner_name}!")
        else:
            await ctx.channel.send(ctx.message.author.mention + ", " + random.choice(eight_ball_responses))

    @commands.command(name='activities',
        description='Random activities for the bored',
        help='Random activities for the bored',
        aliases=['bored'],
        ignore_extra=True,
        hidden=True,
        enabled=True)
    async def activities(self, ctx):
        url = 'https://www.boredapi.com/api/activity/'

        response = requests.request(method='GET', url=url)
        jsonResponse = json.loads(response.text)

        data = jsonResponse['activity'] + "\n"
        if jsonResponse['link']:
            data += jsonResponse['link']

        await ctx.channel.send(data)

    @commands.command(name='bishbot',
        description='Info about Bishbot',
        help='Info about Bishbot',
        ignore_extra=True,
        hidden=True,
        enabled=True)
    async def bishbot(self, ctx):
        await ctx.channel.send(bishbot_text)

    @commands.command(name='breweries',
        description='Breweries as !breweries Santa_Fe',
        help='Breweries as !breweries Santa_Fe',
        aliases=['beer', 'brewery'],
        ignore_extra=True,
        hidden=False,
        enabled=True)
    async def breweries(self, ctx, city):
        url = f"https://api.openbrewerydb.org/breweries?by_city={city}"

        response = requests.request(method='GET', url=url)
        jsonResponse = json.loads(response.text)
        chars = 0

        if jsonResponse:
            data = f"**Breweries in {jsonResponse[0]['city'], jsonResponse[0]['state']}**\n\n"
            for brewery in jsonResponse:
                chars += len(brewery['name']) + len(brewery['brewery_type']) + len(brewery['phone']) + 2 + len(brewery['website_url'])
                if chars >= 1000:
                    await ctx.channel.send(data)
                    data = ''
                    chars = 0
                else:
                    data += f"**{brewery['name']} ({brewery['brewery_type']})**\n"
                    if brewery['street']:
                        data += f"-- {brewery['street']}\n"
                    if brewery['phone']:
                        data += f"-- {brewery['phone'][0:3]}-{brewery['phone'][3:6]}-{brewery['phone'][-4:]}\n"
                    if brewery['website_url']:
                        data += f"-- <{brewery['website_url']}>\n"
            await ctx.channel.send(data)
        else:
            await ctx.channel.send(f"No data found. Make sure to use underscores instead of spaces in city, i.e. Sante_Fe")

    @commands.command(name='busy',
        description="Cat gif to say I'm busy",
        help="Cat gif to say I'm busy",
        ignore_extra=True,
        hidden=False,
        enabled=True)
    async def cat(self, ctx):
        await ctx.channel.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")
        await ctx.channel.send("**I'm Busy!!!**")

    @commands.command(name='jeopardy',
        description="Jeopardy Questions!",
        help="Jeopardy Questions!",
        ignore_extra=True,
        hidden=False,
        enabled=True)
    async def jeopardy(self, ctx):
        url = f"http://jservice.io/api/random"

        response = requests.request(method='GET', url=url)
        jsonResponse = json.loads(response.text)

        if jsonResponse:
            data = f"Q: {jsonResponse[0]['question']}\nA: ||{jsonResponse[0]['answer']}||"
            await ctx.channel.send(data)
        else:
            await ctx.channel.send('Sorry, all outta questions for the moment!')

    @commands.command(name='joke',
        description="Have Waterbot tell you a joke",
        help="Have Waterbot tell you a joke",
        ignore_extra=True,
        hidden=False,
        enabled=True)
    async def joke(self, ctx):
        url = f"https://sv443.net/jokeapi/v2/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist"

        response = requests.request(method='GET', url=url)
        jsonResponse = json.loads(response.text)
        data = ''

        if jsonResponse:
            if jsonResponse['type'] == 'twopart':
                data = f"Q: {jsonResponse['setup']}\nA: {jsonResponse['delivery']}"
            else:
                data += f"{jsonResponse['joke']}"
            await ctx.channel.send(data)
        else:
            await ctx.channel.send('Sorry, all out of jokes for the moment.')

    @commands.command(name='insult',
        description="Insult Generator",
        help=f"Insult Generator, '{BOT_PREFIX}insult @name' to insult someone else",
        aliases=['insult_me', 'insults', 'make_me_cry'],
        ignore_extra=True,
        hidden=False,
        enabled=True)
    async def insult(self, ctx, name="none"):
        if name != "none":
            await ctx.channel.send(name + ", " + random.choice(insult_responses) + "\n     love " + ctx.message.author.mention)
        else:
            await ctx.channel.send(ctx.message.author.mention + ", " + random.choice(insult_responses))

    @commands.command(name='xkcd',
        description="Current xkcd Comic",
        help="Current xkcd Comic",
        ignore_extra=True,
        hidden=False,
        enabled=True)
    async def xkcd(self, ctx):
        url = f"https://xkcd.com/info.0.json"

        response = requests.request(method='GET', url=url)
        jsonResponse = json.loads(response.text)

        if jsonResponse:
            await ctx.channel.send(f"{jsonResponse['img']}")
        else:
            await ctx.channel.send('Sorry, all outta comics for the moment!')


def setup(bot):
    bot.add_cog(Fun(bot))
