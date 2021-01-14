import discord
from discord.ext import commands
import random
import time
import asyncio

class Counting(commands.Cog):
    def __init__(self, avimetry):
        self.avimetry = avimetry

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.avimetry.user:
            return
        if message.guild is None:
            return
        countdoc = self.avimetry.collection.find_one({"_id": "counting"})
        if message.channel.name == "counting":
            if str(message.guild.id) in countdoc:
                if message.author.bot:
                    await message.delete()
                    print("bot")
                elif message.author == self.avimetry.user:
                    print("self")
                    return
                elif message.content != str(countdoc[str(message.guild.id)]):
                    print(countdoc[str(message.guild.id)])
                    await message.delete()
                else:
                    guild=str(message.guild.id)
                    newcount={guild: 1}

                    self.avimetry.collection.update_one({"_id":"counting"}, {"$inc": newcount})

            else:
                guild=str(message.guild.id)
                newguild={guild: 0}
                self.avimetry.collection.update_one({"_id":"counting"}, {"$set":newguild})

    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if message_after.author == self.avimetry.user:
            return
        if message_after.channel.name == "counting":
            if message_before == message_after:
                return
            else:
                await message_after.send(f"Don't Edit Messages, {message_after.author.mention}.", delete_after=5)
                   
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setcount(self, ctx, count : int):
        newcount={str(ctx.guild.id):count}
        self.avimetry.collection.update_one({"$set":newcount})
        await ctx.send(f"Set the count to {count}")     

def setup(avimetry):
    avimetry.add_cog(Counting(avimetry))