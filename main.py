import discord
import os

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



client.run(os.environ['TOKEN'])