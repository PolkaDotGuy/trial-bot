import asyncio
import json
import os
import random
import time
import threading
from datetime import datetime

#from commands import commands
import discord
from discord.ext import commands
#hypixel
import requests

import pytz 
import timer
from dotenv import load_dotenv
from decouple import config
# from keep_alive import keep_alive
# from pathlib import Path

TOKEN = os.getenv('TOKEN')

'''
def GetPrefix(client, message):
	
	Gets prefixes from prefixes.json.

	:param client: bot client
	:type client: discord.ext.commands.bot.Bot

	:param message: user message
	:type message: str

	:return guild_prefix: prefix of guild in which message was sent
	:type guild_prefix: str
	
	with open("prefixes.json", 'r') as f:
		prefixes = json.load(f)
		guild_prefix = prefixes[str(message.guild.id)]
	return guild_prefix
'''

client = commands.Bot(
	command_prefix="t ",
	# intents = discord.Intents(members=True)
	)

'''
@client.event
async def on_guild_join(guild):
	
	Documentation: https://discordpy.readthedocs.io/en/stable/api.html#discord.on_member_join
	
	
	with open("prefixes.json", 'r') as f:
		prefixes = json.load(f)

	prefixes[str(guild.id)] = "t "

	with open("prefixes.json", 'w') as f:
		json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
	with open("prefixes.json", 'r') as f:
		prefixes = json.load(f)

	prefixes.pop(str(guild.id))

	with open("prefixes.json", 'w') as f:
		json.dump(prefixes, f, indent=4)

@client.command()
@commands.has_permissions(administrator=True)
async def ChangePrefix(ctx, prefix):
	with open("prefixes.json", 'r') as f:
		prefixes = json.load(f)

	prefixes[str(ctx.guild.id)] = prefix

	with open("prefixes.json", 'w') as f:
		json.dump(prefixes, f, indent=4)

	await ctx.send(f"Prefix changed to: {prefix}")
	name = f"Prefix: {prefix}"
'''

# Events
@client.event
async def on_ready():
	'''Prints to terminal when bot starts.'''
	print(f'Logged in as {client.user} (ID: {client.user.id})\n------')
	client.loop.create_task(presence())

@client.event
async def presence():
    while True:
        await client.change_presence(activity=discord.Game(name="deeznuts"))
        await asyncio.sleep(10)
        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="beluga videos",
            )
        )
        await asyncio.sleep(10)

@client.event
async def on_message(message):
	if message.guild != None:
		'''
		channelID = message.channel.id
		serverID = message.guild.id
		'''

		if message.author == client.user:
			return
	await client.process_commands(message)

# Commands
@client.command(name="Ping", aliases=["ping", 'p'])
async def Ping(ctx):
	'''Ping command'''
	await ctx.reply(f"Pong! In {round(client.latency * 1000)}ms")

if __name__ == "__main__":
	client.run(TOKEN)