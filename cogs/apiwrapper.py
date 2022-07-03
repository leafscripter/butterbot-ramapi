# TODO: A command that displays information about the requested character (DONE)
# TODO: A command that displays location info (DONE)
# TODO: A command that displays episode info (DONE)
# TODO: Make the code cleaner


from threading import Thread
import requests
import json
import concurrent

from concurrent.futures import ThreadPoolExecutor

import discord
from discord.ext import commands  

import ramapi 
from ramapi import Base 
from ramapi import Character  
from ramapi import Episode 
from ramapi import Location 

# class Helper(): 

#     def __init__(self, threads):
#         self.threads = threads 
#         self.results = []

#     def execute(self, callback, args = None):

#         with ThreadPoolExecutor(max_workers=self.threads) as executor:

#             future_to_url = {executor.submit(callback, args)
            
#             for x in list}

#             for future in concurrent.futures.as_completed(future_to_url):
#                 try:
#                     data = future.result()
#                     self.results.append(data)
#                 except Exception as err:

#                     print("ERROR:", err)

class APIWrapper(commands.Cog):

    def __init__(self, client):
        self.client = client 

        self.characters = ramapi.Character
        self.episodes = ramapi.Episode
        self.locations =  ramapi.Location

        self.character_results = ramapi.Character.get_all()["results"]
        self.episode_results = ramapi.Episode.get_all()["results"]
        self.location_results = ramapi.Location.get_all()["results"]

        self.session = requests.Session()
        # self.helper = Helper(20)

        # self.location 
        self.episode = []
        
        self.embed_color = discord.Color.green()

    @commands.command(name="character")
    async def get_character_info(self, ctx, name = ""):

        if not name: 
            await ctx.send(embed=discord.Embed(
                description="""
                Sorry, but you didn't give me any names to search,

                Use ?list characters
                """,
                color = self.embed_color
            ))
            return

        character : list

        # Check if the name matches any character names in the API
        for result in (self.character_results):
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

            color= self.embed_color
        ).set_image(url=character["image"]))

    @commands.command(name="location") 
    async def get_location_info(self, ctx, name = ""):

        if not name:
            await ctx.send(embed=discord.Embed(
                description = """
                I can't search the database without knowing any names,

                Use ?list locations
                """,
                color = self.embed_color
            )) 

            return

        location : list 

        for result in (self.location_results):
            if name.lower() in result["name"].lower():
                location = result 
                break 

        await ctx.send(embed=discord.Embed(
            title=location["name"],

            description = f"""
            ID: {location["id"]}
            Dimension: {location["dimension"]}
            """,
            color = self.embed_color
        ))



    @commands.command(name="episode")
    async def get_episode_info(self, ctx, name = ""): 

        if not name:
            await ctx.send(embed=discord.Embed(
                description = """
                You're not giving me a whole lot to work with,

                Use ?list episodes
                """,
                color = self.embed_color 
            ))
            return 

        for result in (self.episode_results):
            if name.lower() in result["name"].lower():
                self.episode = result
                break
        
        characters_in_episode = []
        character_description = ""

        # TODO: Implement a more effective method (DONE)
        for character in (self.episode["characters"]): 
            response = self.session.get(character)
            response_json = response.json()
            characters_in_episode.append(response_json["name"])

        for character in (characters_in_episode):
            character_description += character + ", "

        await ctx.send(embed=discord.Embed(
            title= self.episode["name"],
            description= f"""

            Air date: {self.episode["air_date"]}

            Episode: {self.episode["episode"]}

            Characters: {character_description}
            """,
            color = self.embed_color
        ))

    # Determine what the user is requesting 
    # Try to index the class with the request argument 
    # If results are found, list them all in an embed 
    @commands.command(name="list")
    async def list_requested_info(self, ctx, request = "", page = 1):

        if not request or not getattr(self, request):
            await ctx.send(embed=discord.Embed(
                description = """
                It appears that you do not know how to use this command,

                Here is a quick tutorial:

                **?list characters page**    this will list all the characters in the API
                **?list episodes**      this will list all the episodes in the API
                **?list locations**     this will list all the locations in the API
                """,
                
                color = self.embed_color
            ))
            return 

        if page > 42 or page < 1:
            await ctx.send(embed=discord.Embed(
                description = f"""
                There are only 42 pages available, 

                You attemped to index page {page} which does not exist.
                """,
                color = self.embed_color
            ))

        requested_list = ""
        requested_info : list

        count = 1
        count_str = str(count) + ") "

        if request == "characters":
            requested_info = getattr(self, request).get_page(page)["results"]
        else: 
            requested_info = getattr(self, request).get_all()["results"]

        for result in (requested_info):
            requested_list += count_str + result["name"] 
            requested_list += "\n"

            count += 1
            count_str = str(count) + ") "

        await ctx.send(embed=discord.Embed(
            title = f"List of {request}",
            description = requested_list,
            color = self.embed_color
        ))
    
def setup(client):
    client.add_cog(APIWrapper(client))