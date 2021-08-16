import discord
import os
from keep_alive import keep_alive


client = discord.Client()

@client.event
async def on_ready():
  print("i am redy as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('Arcadius'):
    await message.channel.send('Hello!')



keep_alive()
client.run(os.environ['TOKEN'])