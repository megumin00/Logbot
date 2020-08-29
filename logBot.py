# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 15:02:02 2020

@author: User
"""

import discord
import nest_asyncio
import json

class discBot():
    
    def __init__(self):
        self.trusted = [327318597632262149]
        @client.event
        async def on_ready():
            
            print('We have logged in as {0.user}'.format(client))
            
    def readJson(self):
        with open('servers.json', 'r') as openfile: 
            self.jsonObject = json.load(openfile)
            
    def writeJson(self, dictName):
        self.readJson()
        
        tempDict = dictName
        
        tempDict.update(self.jsonObject)

        json_object = json.dumps(tempDict, indent = 4)
        
        with open("servers.json", "w") as outfile: 
            outfile.write(json_object)
            
    def readConvert(self):
        #this only exists so I don't feel sad whenever i try to find what im calling
        self.readJson()
        self.jsonDict = self.jsonObject
    
            
    def serverBind(self):
        @client.event
        async def on_message(message, *args):
            
            self.readConvert()
            self.content = message.content
            self.author = message.author
            self.authorid = message.author.id
            
            if self.content.startswith (';bindserver'):  
                if self.authorid in self.trusted:
                              
                    self.channel = message.channel
                    
                    
                    split = self.content.split()
                    await self.channel.send('logging for {} binded to {}'.format(split[1], self.channel)) 
                    masterDict = {int(split[1]) : message.channel.id}
                    self.writeJson(masterDict)
                    
                else:
                        await self.author.send("you don't have permission to do that :c")
                        
            if self.content.startswith(';help'):
                if self.authorid in self.trusted:
                    helpMessage = ''';help - help
;bindserver (x) - binds all messages from x (server ID) to be sent to this current channel
                        '''
                    await message.channel.send(helpMessage)
                    
                    
                else:
                        await self.author.send("you don't have permission to do that :c")
                    
            if message.author != client.user:
                if str(message.guild.id) in self.jsonDict:
                    loggedChannel = self.jsonDict.get(str(message.guild.id))
                    loggedChannelGet = client.get_channel(loggedChannel)
                    
                    embedVar = discord.Embed(title="Message sent in {}, (ID:{})".format(message.guild, message.guild.id), description='{}'.format(message.content), color=0x00ff00)
                    embedVar.add_field(name="Channel: {}, (ID:{})".format(message.channel, message.channel.id), value='by <@{}> (ID:{})'.format(message.author.id, message.author.id), inline=True)

                    await loggedChannelGet.send(embed=embedVar)
                    
            
    def run(self):
        self.serverBind()
        client.run('bot-token-here')
        
    

if __name__ == "__main__":
    client = discord.Client()
    nest_asyncio.apply()
    
    discBot = discBot()
    discBot.run()

