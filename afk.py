import discord
from discord.ext import commands

'''
Credits to Max Codez:
https://www.youtube.com/watch?v=mpKls9qBg6M
'''

class afk(commands.Cog):
    '''
    afk command
    The bot will reply to other users who mention the user with a preset message.

    :param message (*args): message for people who ping the user
    :type message (*args): str
    '''
    def __init__(self, client):
        self.client = client
        self.data = {}

    @commands.command(name="afk", aliases=[
        "awayfromkeyboard", 
        "away from keyboard", 
        "takingadump", 
        "taking a dump",
        "goout",
        "go out",
        "touching grass"
        ])
    async def afk(self, ctx, *args):
        msg = ' '.join(args)
        self.data[ctx.author.id] = (msg, ctx.channel)
        await ctx.reply("afk set")

    @commands.Cog.listener()
    async def on_message(self, message):
        '''Detects mentions for the user'''
        for id in self.data.keys():
            if (f"<@{id}>" in message.content and not message.author.bot):
                await message.reply(
                    f"They are away right now, they said `{self.data[id][0]}`."
                    )
                break

        if (message.author.id in self.data.keys() and not "afk" in message.content):
            if message.channel != self.data[message.author.id][1]:
                await self.data[message.author.id][1].send(f"<@{message.author.id}> is back!")
            del self.data[message.author.id]
            await message.channel.send(f"<@{message.author.id}> is back!")
    
    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        '''Detects when the user'''
        if (user.id in self.data.keys()):
            if (channel != self.data[user.id][1]):
                await self.data[user.id][1].send(f"<@{user.id}> is back!")
            del self.data[user.id]
            await channel.send(f"<@{user.id}> is back!")

                    
def setup(client):
    client.add_cog(afk(client))