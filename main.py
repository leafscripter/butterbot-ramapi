# Script written by Kaisar Manken 2022

# Import discord modules
import discord
from discord.ext import commands 

# Imports some important modules 
from json import loads 
from pathlib import Path
import os


# Setup the bot
client = commands.Bot(command_prefix=">")
config = loads(Path("config.json").read_text())
token = config["token"]

@client.event
async def on_ready(): 
     print("bot successfully loaded!")

cogfiles = [
     f"cogs.{filename[:-3]}" for filename in os.listdir("./cogs") if filename.endswith(".py")
]

for cogfile in cogfiles:
     try: 
          client.load_extension(cogfile)
     except Exception as error: 
          print(error)

client.run(token)