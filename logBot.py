# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 15:02:02 2020

@author: User
"""

import discord
import nest_asyncio
import json
import asyncio
from discord.ext import commands

class discBot():
    
    def __init__(self):
        self.trusted = [327318597632262149]
        @bot.event
        async def on_ready():
            
            print('We have logged in as {0.user}'.format(bot))
            channelRecipient = bot.get_channel(749641829544230957)
            await channelRecipient.send('Bot online now.')
            
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
            if message.author.id in self.trusted:               
                    
                splitContent = message.message.content.split()
                await message.channel.send('logging for {} binded to {}'.format(splitContent[1], message.channel)) 
                masterDict = {int(splitContent[1]) : message.channel.id}
                self.writeJson(masterDict)
                
        
                
                
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
                    
                
    def adminCommands(self, pass_context=True):
        @bot.command()
        @commands.has_permissions(manage_messages=True)
        async def clear(message, arg):
            messages = []
            
            async for i in message.history(limit=int(arg)+1):
                
                messages.append(i)
                
            await message.channel.delete_messages(messages)
            await message.channel.send('Cleared `{}` Message(s)'.format(arg))

            async for i in message.history(limit=1):
                selfClear = [i]
                await asyncio.sleep(3)
                await message.channel.delete_messages(selfClear)
                
        @bot.command()
        @commands.has_permissions(kick_members=True)
        async def kick(message, arg, *args):
            kickVictim = await bot.fetch_user(arg)
            
            
            kickEmbed = discord.Embed(color=0xFFBDBD)
            kickEmbed.set_author(name='action: User Kicked')

            if args == ():
                kickEmbed.add_field(name='conducted by {}'.format(message.author), value='<@{}> has been kicked'.format(arg))
            else:
                kickReason = ''
                for i in args:
                    kickReason = kickReason + ' ' + i
                kickEmbed.add_field(name='conducted by {}'.format(message.author), value='<@{}> has been kicked for {}'.format(arg, kickReason))
                
            await message.guild.kick(kickVictim, reason=kickReason+' conducted by {}'.format(message.author))
            await message.send(embed=kickEmbed)
            
        @bot.command()
        @commands.has_permissions(ban_members=True)
        async def ban(message, arg, days=0, *args):
            banVictim = await bot.fetch_user(arg)
            
            banEmbed = discord.Embed(color=0xFFBDBD)
            banEmbed.set_author(name='action: User banned')
            
            if int(days) != 0 and args == ():
                banEmbed.add_field(name='conducted by {}'.format(message.author), value='<@{}> has been banned (messages deleted in days: {})'.format(arg, int(days)))
                await message.guild.ban(banVictim, delete_message_days=int(days))
                
            elif days == 0:
                banEmbed.add_field(name='conducted by {}'.format(message.author), value='<@{}> has been banned.'.format(arg))
                await message.guild.ban(banVictim)
                
            else:
                banReason = ''
                for i in args:
                    banReason = banReason + ' ' + i
                banEmbed.add_field(name='conducted by {}'.format(message.author), value='<@{}> has been banned for {} (messages deleted in days: {})'.format(arg, banReason, int(days)))
                await message.guild.ban(banVictim, delete_message_days=int(days), reason=banReason)
                
            await message.send(embed=banEmbed)
                
        
                
        
            
            
    def userCommands(self):
        @bot.command()
        async def ping(message):
            await message.channel.send('pong')
        
        @bot.command()
        async def help(message):
            helpOwner = discord.Embed(color=0xCAFFFF, title="Bot Commands")
            helpOwner.set_author(name='Help has arrived :D',
            icon_url='https://cdn.discordapp.com/attachments/748479776666419223/749449403080900698/chillstolfo.png')
            
            helpOwner.add_field(name=";bindserver (server ID)", value='binds all messages from that server to be redirected to this channel (needs bot inside that server)', inline=True)
            helpOwner.add_field(name=';displayactive', value='displays all active servers for this channel', inline=True)
            helpOwner.set_footer(text="this only exists because I don't comment my code :c")
            
            await message.channel.send(embed=helpOwner)
            
            helpAdmin = discord.Embed(color=0xFFFFCA, title="Admin Commands")
            helpAdmin.add_field(name=';clear (x)', value='clears x amount of messages in chat', inline=True )
            helpAdmin.add_field(name=';kick (targetID) (reason)', value='kicks a member using their ID. Duh.', inline=True )
            helpAdmin.add_field(name=';ban (targetID) (days) (reason)', value='bans a user using their ID. Duh.', inline=True )
            helpAdmin.set_footer(text="this only exists because I don't comment my code :c")
            
            await message.channel.send(embed=helpAdmin)
            
            helpUser = discord.Embed(color=0xBDFFBD, title='User Commands')
            helpUser.add_field(name=";help", value='prints out this menu', inline=True)
            helpUser.add_field(name=";ping", value='pong?', inline=True )
            helpUser.set_footer(text="this only exists because I don't comment my code :c")
            
            await message.channel.send(embed=helpUser)
            
            moreInfo = discord.Embed(title='https://github.com/megumin00/authoritarian-dictatorship-discbot')
            
            await message.channel.send(embed=moreInfo)
                
        
            
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
                    embedVar.add_field(name="Channel: {}, (ID:{})".format(message.channel, message.channel.id), value='by <@!{}>, <#{}> (ID:{})'.format(message.author.id, message.channel.id, message.author.id), inline=True)
    
                    await loggedChannelGet.send(embed=embedVar)
                        
                        
                await bot.process_commands(message)
                    
            
    def run(self):
        self.trustedCommands()
        self.adminCommands()
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
