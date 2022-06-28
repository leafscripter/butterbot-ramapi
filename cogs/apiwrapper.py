# TODO: A command that displays information about the requested character 
# TODO: A command that displays location info 
# TODO: A command that displays episode info 

import discord
from discord.ext import commands  

import ramapi 
from ramapi import Base 
from ramapi import Character  
from ramapi import Episode 
from ramapi import Location 

class APIWrapper(commands.Cog):

    def __init__(self, client):
        self.client = client 

        self.characters = ramapi.Character.get_all()["results"]
        self.episodes = ramapi.Episode.get_all()["results"]
        self.locations =  ramapi.Location.get_all()["results"]

    @commands.command(name="character")
    async def get_character_info(self, ctx, name = ""):

        character : list

        # Check if the name matches any character names in the API
        for result in (self.characters):
            if name.lower() in result["name"].lower():
                character = result
                break

        await ctx.send(embed=discord.Embed(
            title=character["name"],

            description = f"""
            Species: {character["species"]}
            Gender: {character["gender"]}
            Status: {character["status"]} 
            Origin: {character["origin"]["name"]}
            """,

            color=discord.Color.purple()
        ).set_image(url=character["image"]))

    @commands.command(name="location") 
    async def get_location_info(self, ctx, name = ""):
        location : list 

        for result in (self.locations):
            if name.lower() in result["name"].lower():
                location = result 
                break 

        await ctx.send(embed=discord.Embed(
            title=location["name"],

            description = f"""
            ID: {location["id"]}
            Dimension: {location["dimension"]}
            """,
            color = discord.Color.purple()
        ))

    @commands.command(name="episode")
    async def get_episode_info(self, ctx, name): 
        
        episode : list 

        for result in (self.episodes):
            if name.lower() in result["name"].lower():
                episode = result 
                break 

        await ctx.send(embed=discord.Embed(
            title=episode["name"],
            description= f"""

            Unfortunately,

            The Rick and Morty API does not provide much information,

            This was all that I could find :/

            Air date: {episode["air_date"]}
            Episode: {episode["episode"]}
            """,
            color = discord.Color.purple()
        ))

    
def setup(client):
    client.add_cog(APIWrapper(client))
        

        