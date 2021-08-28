#imports
import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
import datetime
from replit import db



#intents to let on_member_join/on_member_remove work
intents = discord.Intents.default()
intents.members = True

#client instance initiated
client = commands.Bot(command_prefix = {'Arcadius ','arcadius ','arc ','Arc ','ar ','Ar '}, intents=intents)

#redy message
@client.event
async def on_ready():
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



#keep alive loop
keep_alive()
client.run(os.environ['TOKEN'])