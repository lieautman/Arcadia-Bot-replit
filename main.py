#imports
import discord
from discord.ext import commands, tasks
from keep_alive import keep_alive
import os
import datetime
from replit import db
import replit


#intents to let on_member_join/on_member_remove work
intents = discord.Intents.default()
intents.members = True

#client instance initiated
client = commands.Bot(command_prefix = {'Arcadius ','arcadius ','arc ','Arc ','ar ','Ar '}, intents=intents)

#redy message
@client.event
async def on_ready():
  replit.clear()
  print("i am redy as {0.user}".format(client))


#get time for storage
now=datetime.datetime.now()
print("Current date and time is:")
print(now.strftime("%y-%m-%d %H:%M:%S"))


#on join
@client.event
async def on_member_join(member):
  now=datetime.datetime.now()
  print(f'{member} has joined the server at ')
  print(now.strftime("%y-%m-%d %H:%M:%S."))
  db[f'{member}'] = now.strftime("%y-%m-%d %H:%M:%S.")
  keys = db.keys()
  print(keys)

#on leave
@client.event
async def on_member_remove(member):
  now=datetime.datetime.now()
  print(f'{member} has left the server at ')
  print(now.strftime("%y-%m-%d %H:%M:%S."))
  del db[f'{member}']
  keys = db.keys()
  print(keys)


#clear text command
@client.command()
async def clear(ctx, amount=5):
  await ctx.channel.purge(limit=amount+1)
  print(f'Removed {amount} messages')

#kick command
@client.command()
async def kick(ctx, member : discord.Member,*, reason=None):
  await member.kick(reason=reason)

#hi command
@client.command()
async def hello(ctx):
  await ctx.channel.send('Hello!')


#music pleya
from discord.voice_client import VoiceClient
import youtube_dl

from random import choice
import time

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        #print("Playing "+data['title'])

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        if os.path.exists("Muzica.webm"):
          os.remove("Muzica.webm")
        os.rename(filename,"Muzica.webm")

        return cls(discord.FFmpegPCMAudio("Muzica.webm", **ffmpeg_options), data=data)



def is_connected(ctx):
    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()


import queue
q = queue.Queue()

@client.command(name='play', help='This command plays music')
async def play(ctx,*, url):

  if not ctx.message.author.voice:
    await ctx.send("You are not connected to a voice channel")
    return

  else:
    channel = ctx.message.author.voice.channel

  if not is_connected(ctx):
    await channel.connect()

  await play_song(ctx,url)

async def play_song(ctx,url,):
  server = ctx.message.guild
  voice_channel = server.voice_client

  async with ctx.typing():
    player = await YTDLSource.from_url(url, loop=client.loop)


  voice_channel.play(player, after=lambda error: client.loop.create_task(check_queue(ctx)))

  await ctx.send('**Now playing:** {}'.format(player.title))

async def check_queue(ctx):
  if q.empty()!=1:
    url=q.get()
    await play_song(ctx, url)

@client.command(name='queue', help='This command queues up next song')
async def queue(ctx,*, url):
  q.put(url)


@client.command(name='stop', help='This command stops the music and makes the bot leave the voice channel')
async def stop(ctx):
  while(q.empty()!=1):
    q.get()
  os.remove("Muzica.webm")
  voice_client = ctx.message.guild.voice_client
  await voice_client.disconnect()



#keep alive loop
keep_alive()
client.run(os.environ['TOKEN'])