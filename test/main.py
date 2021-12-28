import discord
from discord.ext import commands


intents = discord.Intents.default()

client = commands.Bot(command_prefix='a.', intents=intents)
client.remove_command('help')

token = ''
client.run(token)
