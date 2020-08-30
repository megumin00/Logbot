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
                helpOwner = discord.Embed(color=0xCAFFFF, title="Bot Commands")
                helpOwner.set_author(name='Help has arrived :D',
                icon_url='https://cdn.discordapp.com/attachments/748479776666419223/749449403080900698/chillstolfo.png')
                    
                helpOwner.add_field(name=";help", value='prints out this menu', inline=True)
                helpOwner.add_field(name=";bindserver (server ID)", value='binds all messages from that server to be redirected to this channel (needs bot inside that server)', inline=True)
                helpOwner.add_field(name=';displayactive', value='displays all active servers for this channel', inline=True)
                helpOwner.set_footer(text="this only exists because I don't comment my code :c")
                    
                await message.channel.send(embed=helpOwner)
                
                helpAdmin = discord.Embed(color=0xFFFFCA, title="Admin Commands")
                helpAdmin.add_field(name=';clear (x)', value='clears x amount of messages in chat', inline=True )
                helpAdmin.set_footer(text="this only exists because I don't comment my code :c")
                
                await message.channel.send(embed=helpAdmin)
                
                helpUser = discord.Embed(color=0xBDFFBD, title='User Commands')
                helpUser.add_field(name=";ping", value='pong?', inline=True )
                helpUser.set_footer(text="this only exists because I don't comment my code :c")
                
                await message.channel.send(embed=helpUser)
                
                
                
        @bot.command()
        async def displayactive(message):
            if message.author.id in self.trusted:
                self.readJson()
                self.displayActive = discord.Embed(color=0xBD5CFF)
                self.displayActive.set_author(name="Servers being Tracked".format(message.guild, message.guild.id),
                icon_url='https://cdn.discordapp.com/attachments/748479776666419223/749449403080900698/chillstolfo.png')
                for i in self.jsonDict:
                    displayGuild = bot.get_guild(int(i))
                    self.displayActive.add_field(name='Server: {}'.format(displayGuild), value='channel: <#{}>'.format(self.jsonDict[i]), inline=True)
                    
                await message.channel.send(embed=self.displayActive)
                    
                '''
    def adminCommands(self):
        @bot.command()
        async def clear(message, args):
            
        
        
    def userCommands(self):'''
        
        
            
    def serverLog(self): 
        @bot.event
        async def on_message(message):
            if message.author != bot.user:
                self.readJson()
                if str(message.guild.id) in self.jsonDict:
                    loggedChannel = self.jsonDict.get(str(message.guild.id))
                    loggedChannelGet = bot.get_channel(loggedChannel)
                        
                    embedVar = discord.Embed(title="{}".format(message.content), color=0xFFCAFF)
                    embedVar.set_author(name="Message sent in {}, (ID:{})".format(message.guild, message.guild.id),
                    icon_url='https://cdn.discordapp.com/attachments/748479776666419223/749449403080900698/chillstolfo.png')
                    embedVar.add_field(name="Channel: {}, (ID:{})".format(message.channel, message.channel.id), value='by <@{}>, <#{}> (ID:{})'.format(message.author.id, message.channel.id, message.author.id), inline=True)
    
                    await loggedChannelGet.send(embed=embedVar)
                        
                        
                await bot.process_commands(message)
                    
            
    def run(self):
        self.trustedCommands()
        self.adminComamnds()
        self.userCommands()
        self.serverLog()
        
        bot.run('')
        
    

if __name__ == "__main__":
    client = discord.Client()   
    bot = commands.Bot(command_prefix=';')
    bot.remove_command('help')
    nest_asyncio.apply()
    
    
    discBot = discBot()
    discBot.run()
