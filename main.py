# Script written by Kaisar Manken 2022

# TODO: Add a command that displays episode info (DONE)
# TODO: Add a command that displays location info 
# TODO: Try to make the code cleaner 

# Import discord modules
import discord
from discord.ext import commands 

# Import the API modules
import ramapi 

from ramapi import Base
from ramapi import Character
from ramapi import Episode

# Import variables from the config file 
from json import loads 
from pathlib import Path

config = loads(Path("config.json").read_text())

# Setup the bot
bot = commands.Bot(command_prefix=">")
token = config["token"]

api_characters  = ramapi.Character.get_all()
api_episodes = ramapi.Episode.get_all()
api_locations = ramapi.Location.get_all()

def make_embed(title: str, description: str, color: discord.Color): 
    return discord.Embed(
        title = title, 
        description = description,
        color = color
    )

def generate_description(name, status, species, origin): 
    return f"{name} is a {species.lower()} originating from {origin}. As of season 5, he is {status.lower()}"

@bot.event
async def on_ready(): 
     print("bot successfully loaded!")
    
@bot.command(name='character')
async def get_character_info(ctx, name):

    character_info : list 
    
    for result in (api_characters ["results"]):
        if name.lower() in result["name"].lower():
            character_info = result
            break

    character_name = character_info["name"]
    character_status = character_info["status"]
    character_species = character_info["species"]
    character_origin = character_info["origin"]["name"]

    info_embed = make_embed(
        "About character",
        generate_description(character_name, character_status, character_species, character_origin), 
        discord.Color.purple()
    )

    info_embed.set_image(url=character_info["image"])

    await ctx.send(embed = info_embed)


@bot.command(name="episode")
async def get_episode_info(ctx, episode):

    episode_info : list 

    for result in (api_episodes["results"]):
        if (episode.lower() == result["name"].lower()) or (episode.lower() in result["name"].lower()):
            episode_info = result 
            break 

    episode_name = episode_info["name"]
    episode_date = episode_info["air_date"]

    info_embed = discord.Embed(
        title = episode_name,
        description = f'This episode was released in {episode_date}',
        color = discord.Color.purple()
    )

    await ctx.send(embed = info_embed)

@bot.command(name="alive")
async def get_alive_info(ctx):
    
    alive_characters = ramapi.Character.filter(status="alive")
    character_list = []

    for character in alive_characters:
        character_list.append(character)

    count = len(character_list)

    info_embed = discord.Embed(
        title = "Characters that are still alive",
        description = f"As of season 5, there are {count} characters that are alive",
        color = discord.Color.purple()
    )

    await ctx.send(embed=info_embed)

bot.run(token)