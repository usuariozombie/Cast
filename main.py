# -*- coding: utf-8 -*-

import nextcord
from nextcord.ext import commands
from utils import Debug, JSON, ClearScreen, PurgeCache

ConfigData = JSON.Read("config.json")

PurgeCache(), ClearScreen(True)
Debug.Info("Connecting...")

client = commands.Bot(case_insensitive = True, command_prefix = ConfigData["Prefix"], intents = nextcord.Intents.all())
client.remove_command("help")

try: client.load_extension("weather")
except Exception as Error: Debug.Error(f"An error has occured while loading the weather.py\n{Error}")

@client.event
async def on_ready():
	Debug.Good(f"Connected as {client.user.name}#{client.user.discriminator} ({client.user.id})!")
	Debug.Line(f"Currently in {str(len(client.guilds))} servers using \"{ConfigData['Prefix']}\" as prefix.")
	Debug.Line(f"https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions={ConfigData['Permissions']}&scope=applications.commands%20bot\n")

@client.command()
async def load(ctx):
	if ctx.author.id in JSON.Read("config.json")["Whitelist"]:
		try: client.load_extension("weather"); await ctx.send(f"> Loaded successfully!")
		except Exception as Error: await ctx.send(f"> **An error has occurred while loading: ```\n{Error}```")

@client.command()
async def reload(ctx):
	if ctx.author.id in JSON.Read("config.json")["Whitelist"]:
		try: client.reload_extension("weather"); await ctx.send(f"> Reloaded successfully!")
		except Exception as Error: await ctx.send(f"> **An error has occurred while reloading: ```\n{Error}```")

@client.command()
async def unload(ctx):
	if ctx.author.id in JSON.Read("config.json")["Whitelist"]:
		try: client.unload_extension("weather"); await ctx.send(f"> Unloaded successfully!")
		except Exception as Error: await ctx.send(f"> **An error has occurred while unloading: ```\n{Error}```")

client.run(ConfigData["BotToken"]), PurgeCache()