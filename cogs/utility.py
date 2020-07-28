#! /usr/bin/env python3

"""
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

import discord
import json
import os
import requests
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
BOT_PREFIX = os.getenv('DISCORD_BOT_PREFIX')
GUILD = os.getenv('DISCORD_GUILD')
AIRVISUAL_KEY = os.getenv('AIRVISUAL_KEY')


class Utility(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('- Utility Cog loaded')

    @commands.command(name='ban',
        description='Ban member from server',
        help='Ban member from server',
        ignore_extra=True,
        hidden=True,
        enabled=False)
    async def ban(self, ctx, member: discord.member, *, reason=None):
        if member.hasPermission('BAN_MEMBERS'):
            await member.ban(reason=reason)
            await ctx.send(f"Banned {member.mention}")

    @commands.command(name='clear',
        description='Clear x messages, defaults to 3',
        help='Clear x messages, defaults to 3',
        ignore_extra=True,
        hidden=False,
        enabled=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=3):
        await ctx.channel.purge(limit=amount)

    @commands.command(name='ip_abuse',
        description='Get abuse score for IP',
        help='Get abuse score for IP',
        ignore_extra=True,
        hidden=False,
        enabled=True)
    async def ip_abuse(self, ctx, ipAddress):
        ABUSEIPDB_KEY = os.getenv('ABUSEIPDB_KEY')
        url = 'https://api.abuseipdb.com/api/v2/check'

        querystring = {
            'ipAddress': ipAddress,
            'maxAgeInDays': '90'
        }

        headers = {
            'Accept': 'application/json',
            'Key': ABUSEIPDB_KEY
        }

        response = requests.request(method='GET', url=url, headers=headers, params=querystring)
        ip_info = json.loads(response.text)

        data = '**Data provided by abuseipdb.com**\n\n'
        for k, v in ip_info['data'].items():
            data += f"{k}: {v}\n"

        await ctx.channel.send(data)

    @commands.command(name='kick',
        description='Kick member off server',
        help='Kick member off server',
        ignore_extra=True,
        hidden=True,
        enabled=False)
    async def kick(self, ctx, member: discord.member, *, reason=None):
        if member.hasPermission('KICK_MEMBERS'):
            await member.kick(reason=reason)
            await ctx.send(f"Kicked {member.mention}")

    @commands.command(name='member',
        description='Member information',
        help='Member information',
        ignore_extra=True,
        hidden=False,
        enabled=True)
    async def member(self, ctx, mention):
        guild = discord.utils.get(self.bot.guilds, name=GUILD)
        for member in guild.members:
            if str(member.id) == str(mention.lstrip('<@!').rstrip('>')):
                await ctx.channel.send(f"Nickname: {member.nick}\n"
                    f"Discord Name: {member.name}#{member.discriminator}\n"
                    f"Discord ID: {member.id}\n"
                    f"Joined: {member.joined_at}\n"
                    f"Status: {member.status}\n"
                    # f"Is on Mobile: {member.is_on_mobile}\n"
                    # f"Activity: {str(member.activity.type).lstrip('ActivityType.')} {member.activity.name}\n"
                    f"Guild: {member.guild}\n"
                    f"Guild Permissions: {member.guild_permissions}\n"
                    f"Top Role: {member.top_role}\n"
                    f"Roles: {str(', '.join([role.name for role in member.roles]).replace('@', ''))}\n")

    @commands.command(name='members',
        description='Current Members',
        help='Current Members',
        ignore_extra=True,
        hidden=False,
        enabled=True)
    async def members(self, ctx, showall=None):
        guild = discord.utils.get(self.bot.guilds, name=GUILD)
        members = ''
        for member in guild.members:
            if showall == 'showall':
                members += f"- {member.display_name} : "
                members += f"{member.name} ("
                members += ', '.join([role.name for role in member.roles]) + ")\n"
            else:
                members += f"- {member.display_name}\n"
        await ctx.channel.send(f"**Server Members: {guild.member_count}**\n{members.replace('@', '')}")

    @commands.command(name='nickname',
        description='Change nickname',
        help='Change nickname',
        ignore_extra=True,
        hidden=False,
        enabled=True)
    async def nickname(self, ctx, *, nickname):
        await ctx.author.edit(nick=f"{nickname}")
        # role = get(ctx.message.server.roles, name='ROLE_NAME')
        # if role: # If get could find the role
        #     await client.add_role(ctx.message.author, role)

    @commands.command(name='ping',
        description='Ping latency',
        help='Ping latency',
        ignore_extra=True,
        hidden=False,
        enabled=True)
    async def ping(self, ctx):
        await ctx.channel.send(f"Pong... {round(self.bot.latency * 1000)} ms")

    @commands.command(name='server',
        description='Server information',
        help='Server information',
        ignore_extra=True,
        hidden=False,
        enabled=True)
    # @commands.has_role('admins')
    async def server(self, ctx):
        guild = discord.utils.get(self.bot.guilds, name=GUILD)
        text_channels = '\n - '.join([channel.name for channel in guild.text_channels])
        voice_channels = '\n - '.join([channel.name for channel in guild.voice_channels])
        members = '\n - '.join([member.name for member in guild.members])
        await ctx.channel.send(f"Server Name: {guild.name} (ID: {guild.id})\n"
                            f"Server Owner: {guild.owner} (ID: {guild.owner_id})\n"
                            f"Server Description: {guild.description}\n"
                            f"Region: {guild.region}\n"
                            f"File Size Limit: {guild.filesize_limit} bytes\n\n"
                            f"**Text Channels:**\n - {text_channels}\n\n"
                            f"**Voice Channels:**\n - {voice_channels}\n\n"
                            f"**Server Members: {guild.member_count}**\n - {members}")

    @commands.command(name='unban',
        description='Unban member from server',
        help='Unban member from server',
        ignore_extra=True,
        hidden=True,
        enabled=False)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"Unbanned {user.mention}")
                return

    @commands.command(name='weather',
        description='Weather as !weather CITY STATE',
        help='Weather as !weather Santa_Fe New_Mexico',
        ignore_extra=True,
        hidden=True,
        enabled=True)
    async def weather(self, ctx, city, state):
        # This intended as a 'good enough' tool. There are some accuracy issues
        # such as conversion of C to F temps and wind_mapping where NNE is
        # actually 11.25 - 33.75 degrees vs the ints required by range().
        url = f"https://api.airvisual.com/v2/city?city={city.replace('_', '%20')}&state={state.replace('_', '%20')}&country=USA&key={AIRVISUAL_KEY}"

        response = requests.request(method='GET', url=url)
        jsonResponse = json.loads(response.text)

        if jsonResponse['status'] == 'success':
            weather_mapping = {'01': 'Clear Sky',
                            '02': 'Few Clouds',
                            '03': 'Scattered Clouds',
                            '04': 'Broken Clouds',
                            '09': 'Shower Rain',
                            '10': 'Rain',
                            '11': 'Thunderstorm',
                            '13': 'Snow',
                            '50': 'Mist'}

            aqius_mapping = {'Good': range(0, 50),
                            'Moderate': range(51, 100),
                            'Unhealthy for Sensitive Groups': range(101, 150),
                            'Unhealthy': range(151, 200),
                            'Very Unhealthy': range(201, 300),
                            'Hazardous': range(301, 500)}

            wind_mapping = {'North': range(349, 360),
                            'N': range(0, 11),
                            'NNE': range(12, 34),
                            'NE': range(35, 56),
                            'ENE': range(57, 79),
                            'E': range(80, 101),
                            'ESE': range(102, 124),
                            'SE': range(125, 146),
                            'SSE': range(147, 169),
                            'S': range(170, 191),
                            'SSW': range(192, 214),
                            'SW': range(215, 236),
                            'WSW': range(237, 259),
                            'W': range(260, 281),
                            'WNW': range(282, 304),
                            'NW': range(305, 326),
                            'NNW': range(327, 348)}

            data = f"{jsonResponse['data']['city']}, {jsonResponse['data']['state']}, {jsonResponse['data']['country']}\n"
            data += f"{jsonResponse['data']['location']['coordinates']}\n"

            # ic comes through like 01d or 01n to differentiate day or night, we don't care
            # so we're just mapping the numerical part to the human friendly text version.
            data += f"{weather_mapping[jsonResponse['data']['current']['weather']['ic'][:-1]]}\n"

            # Print out the AQIUS then do a map to ranges and print out a human friendly
            # equivilant.
            data += f"Air Quality Index: {jsonResponse['data']['current']['pollution']['aqius']} - "
            for key, val in aqius_mapping.items():
                if int(jsonResponse['data']['current']['pollution']['aqius']) in val:
                    data += f"{key}\n"

            data += f"Temperature: {int(((jsonResponse['data']['current']['weather']['tp']) * 9) / 5) + 32}°F\n"
            data += f"Pressure: {jsonResponse['data']['current']['weather']['pr']} hPa\n"
            data += f"Humidity: {jsonResponse['data']['current']['weather']['hu']}%\n"
            data += f"Wind: {int(jsonResponse['data']['current']['weather']['ws'] * 2.236936)} m/h from "

            for key, val in wind_mapping.items():
                if int(jsonResponse['data']['current']['weather']['wd']) in val:
                    data += f"{jsonResponse['data']['current']['weather']['wd']}° ({key})\n"
            await ctx.channel.send(data)
        else:
            await ctx.channel.send(f"No data found. Make sure to use underscores instead of spaces in city or state, i.e. Sante_Fe New_Mexico")

    @commands.command(name='whoami',
        description='Info about you',
        help='Info about you',
        ignore_extra=True,
        hidden=True,
        enabled=True)
    async def whoami(self, ctx):
        await ctx.channel.send(f"User Name: {ctx.author.name}\nUser ID: {ctx.author.id}")


def setup(bot):
    bot.add_cog(Utility(bot))
