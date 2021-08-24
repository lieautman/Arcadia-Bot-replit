#imports
import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
import datetime


#intents to let on_member_join/on_member_remove work
intents = discord.Intents.default()
intents.members = True

#client instance initiated
client = commands.Bot(command_prefix = 'Arcadius ', intents=intents)

#redy message
@client.event
async def on_ready():
  print("i am redy as {0.user}".format(client))


#on join
@client.event
async def on_member_join(member):
  print(f'{member} has joined the server.')

#on leave
@client.event
async def on_member_remove(member):
  print(f'{member} has left the server.')

#first try
#@client.event
#async def on_message(message):
#  if message.author == client.user:
#    return

  #if message.content.startswith('Arcadius'):
  #  await message.channel.send('Hello!')


#clear text command
@client.command()
async def clear(ctx, amount=5):
  await ctx.channel.purge(limit=amount+1)
  print(f'Removed {amount} messages')

#kick command
@client.command()
async def kick(ctx, member : discord.Member,*, reason=None):
  await member.kick(reason=reason)


#keep alive loop
keep_alive()
client.run(os.environ['TOKEN'])