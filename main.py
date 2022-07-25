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
import afk


def GetPrefix(client, message):
	'''
	https://stackoverflow.com/a/64513681
	Gets prefixes from prefixes.json.

	:param client: bot client
	:type client: discord.ext.commands.bot.Bot

	:param message: user message
	:type message: str

	:return guild_prefix: prefix of guild in which message was sent
	:type guild_prefix: str
	'''
	with open("prefixes.json", 'r') as f:
		prefixes = json.load(f)
		guild_prefix = prefixes[str(message.guild.id)]
	return guild_prefix

intents = discord.Intents.default()
intents.members = True
intents.presences = True
client = commands.Bot(
	command_prefix=GetPrefix,
	intents = intents, 
	strip_after_prefix=True
	)

'''Setup cogs'''
cogs = [afk]
for cog in cogs:
	cog.setup(client)


# Events
@client.event
async def on_guild_join(guild):
	'''
	https://stackoverflow.com/a/64513681
	Documentation: https://discordpy.readthedocs.io/en/stable/api.html#discord.on_guild_join
	Adds default guild prefix ("t ") to prefixes.json when bot joins server
	'''
	
	print(f"Joined {guild.name}!")

	with open("prefixes.json", 'r') as f:
		prefixes = json.load(f)

	prefixes[str(guild.id)] = "t "

	with open("prefixes.json", 'w') as f:
		json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
	'''
	https://stackoverflow.com/a/64513681
	Removes guild prefix from prefixes.json when bot leaves server
	'''
	with open("prefixes.json", 'r') as f:
		prefixes = json.load(f)

	prefixes.pop(str(guild.id))

	with open("prefixes.json", 'w') as f:
		json.dump(prefixes, f, indent=4)

@client.event
async def on_message(message):
	'''Processes every message'''
	if (message.guild != None):
		'''
		channelID = message.channel.id
		serverID = message.guild.id
		'''

		if (message.author == client.user):
			return
	await client.process_commands(message)

@client.event
async def on_ready():
	'''Prints to terminal when bot starts.'''
	print(f'Logged in as {client.user} (ID: {client.user.id})\n------')
	client.loop.create_task(presence())

@client.event
async def presence():
	'''Cycles between presences.'''
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


# Commands
@client.command(name="Ping", aliases=["ping", 'p'])
async def Ping(ctx):
	'''Ping command'''
	await ctx.reply(f"Pong! In {round(client.latency * 1000)}ms")

@client.command(name="ChangePrefix", aliases=["changeprefix", "prefix"])
@commands.has_permissions(administrator=True)
async def ChangePrefix(ctx, prefix):
	'''
	https://stackoverflow.com/a/64513681
	Changes prefix for a server

	:param prefix: New server prefix
	:type prefix: str
	'''
	with open("prefixes.json", 'r') as f:
		prefixes = json.load(f)

	prefixes[str(ctx.guild.id)] = prefix

	with open("prefixes.json", 'w') as f:
		json.dump(prefixes, f, indent=4)

	await ctx.send(f"Prefix changed to: `{prefix}`.")
	name = f"Prefix: {prefix}"

@client.command(aliases=["exit"])
@commands.is_owner()
async def Exit(ctx):
	'''Exit command'''
	await ctx.send("Goodbye...")
	exit()

load_dotenv()
TOKEN = os.getenv('TOKEN')
if (__name__ == "__main__"):
	client.run(TOKEN)