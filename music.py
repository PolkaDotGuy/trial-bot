import discord
from discord.ext import commands
import youtube_dl
import pafy

class music(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def disconnect(self, ctx):
		'''Disconnects from voice call'''
		await ctx.voice_client.disconnect()

	@commands.command()
	async def play(self, ctx, url):
		'''Plays URL in voice channel'''

		'''Checks if bot and user are in voice channels'''
		if (ctx.author.voice is None):
			await ctx.send("You're not in a voice channel!")
		voice_channel = ctx.author.voice.channel
		if (ctx.voice_client is None):
			await voice_channel.connect()
		else:
			await ctx.voice_client.move_to(voice_channel)

		ctx.voice_client.stop() # Stops previous song before starting a new one
		FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 reconnect_delay_max 5','options': '-vn'}
		YDL_OPTIONS = {
		'format': 'bestaudio'
		}
		
		with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
			info = ydl.extract_info(url, download = False)
			await ctx.send("work")
			source_url = info['formats'][0]['url']
			print(source_url)
			source = await discord.FFmpegOpusAudio.from_probe(source_url, method='fallback') #, **FFMPEG_OPTIONS)
			# source = pafy.new(url).getbestaudio().url # maybe we could use pafy
			ctx.voice_client.play(source)

	@commands.command()
	async def pause(self, ctx):
		'''Pauses current song'''
		await ctx.voice_client.pause()
		await ctx.send("Paused")

	@commands.command()
	async def resume(self, ctx):
		'''Resumes song after pausing'''
		await ctx.voice_client.resume()
		await ctx.send("Resuming")


def setup(client):
	client.add_cog(music(client))