# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 15:02:02 2020

@author: User
"""

import discord
import nest_asyncio
import json
from discord.ext import commands

class discBot():
    
    def __init__(self):
        self.trusted = [327318597632262149]
        @bot.event
        async def on_ready():
            
            print('We have logged in as {0.user}'.format(bot))
            
    def readJson(self):
        with open('servers.json', 'r') as openfile: 
            self.jsonDict = json.load(openfile)
            
    def writeJson(self, dictName):
        self.readJson()
        
        tempDict = dictName
        
        tempDict.update(self.jsonDict)

        json_object = json.dumps(tempDict, indent = 4)
        
        with open("servers.json", "w") as outfile: 
            outfile.write(json_object)
        
    def trustedCommands(self):
        @bot.command()
        async def test(message, arg):
            if message.author.id in self.trusted:
                await message.send(arg)
                
        @bot.command()
        async def bindserver(message):
            self.readJson()
            print(message)
            if message.author.id in self.trusted:               
                    
                splitContent = message.message.content.split()
                await message.channel.send('logging for {} binded to {}'.format(splitContent[1], message.channel)) 
                masterDict = {int(splitContent[1]) : message.channel.id}
                self.writeJson(masterDict)
                
        @bot.command()
        async def help(message):
            if message.author.id in self.trusted:
                helpMessage = discord.Embed(color=0x00FFFF)
                helpMessage.set_author(name='help has arrived',
                icon_url='https://cdn.discordapp.com/attachments/748479776666419223/749449403080900698/chillstolfo.png')
                    
                helpMessage.add_field(name=";help", value='prints out this menu')
                helpMessage.add_field(name=";bindserver (server ID)", value='binds all messages from that server to be redirected to this channel (needs bot inside that server)')
                helpMessage.add_field(name=';dispalyactive', value='displays all active servers for this channel')
                    
                await message.channel.send(embed=helpMessage)
                
            
    def serverLog(self): 
        @bot.event
        async def on_message(message):
            if message.author != bot.user:
                self.readJson()
                if str(message.guild.id) in self.jsonDict:
                    loggedChannel = self.jsonDict.get(str(message.guild.id))
                    loggedChannelGet = bot.get_channel(loggedChannel)
                        
                    embedVar = discord.Embed(title="{}".format(message.content), color=0x00ff00)
                    embedVar.set_author(name="Message sent in {}, (ID:{})".format(message.guild, message.guild.id))
                    embedVar.add_field(name="Channel: {}, (ID:{})".format(message.channel, message.channel.id), value='by <@{}> (ID:{})'.format(message.author.id, message.author.id), inline=True)
    
                    await loggedChannelGet.send(embed=embedVar)
                        
                        
                await bot.process_commands(message)
                    
            
    def run(self):
        self.trustedCommands()
        self.serverLog()
        
        bot.run('')
        
    

if __name__ == "__main__":
    client = discord.Client()   
    bot = commands.Bot(command_prefix=';')
    bot.remove_command('help')
    nest_asyncio.apply()
    
    
    discBot = discBot()
    discBot.run()
