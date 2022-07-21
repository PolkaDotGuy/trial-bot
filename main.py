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

client = commands.Bot(
	command_prefix="t ",
	# intents = discord.Intents(members=True)
	)

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