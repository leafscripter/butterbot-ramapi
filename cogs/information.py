# TODO: A command explaining how to use the bot (DONE)

import discord  
from discord.ext import commands

class Information(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="helpme")
    async def display_help_message(self, ctx): 

        info_embed = discord.Embed(
            title = "Help",
            description = """ 
            Greetings master!

            Here is a list of commands to get you started:

            >character name -> this command displays character information 
            >episode name -> this command displays episode information 
            >location name -> this command displays location information 

            >helpme -> use this command if you forget the commands
            
            Well that is all!
            
            """,

            color = discord.Color.purple()
            ) 

        await ctx.send(embed = info_embed)

def setup(client):
    client.add_cog(Information(client))