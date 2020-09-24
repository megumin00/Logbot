# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 15:02:02 2020

@author: User
"""


'''
TODOS

'''
import discord
import nest_asyncio
import json
import asyncio
import random
import logging
from discord.ext import commands

class discBot():
    
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.trusted = [327318597632262149]
        self.annoyList = []
        self.ID = ''
        @bot.event
        async def on_ready():
            
            print('We have logged in as {0.user}'.format(bot))
            channelRecipient = bot.get_channel(749641829544230957)
            await channelRecipient.send('Bot online now.')
            
            
    def mentionOrID(self, args):
            forbidden = ['<', '>', '@', '!']
            ID = ''
            allow = bool
            
            try:
                if type(int(args)) == int:
                    allow = True
                    
            except ValueError:
                allow = False
            
            if allow == True:
                ID = args

            else:
                for i in args:
                    if i not in forbidden:
                        ID += i
                        
            self.ID = ID
            
            
    def readJson(self, jsonFile):
        with open(jsonFile, 'r') as openfile: 
            self.jsonDict = json.load(openfile)
            
            
    def writeJson(self, dictName, jsonFile):
        self.readJson(jsonFile)
        tempDict = dictName
        self.jsonDict.update(tempDict)

        json_object = json.dumps(self.jsonDict, indent = 4)
        
        with open(jsonFile, "w") as outfile: 
            outfile.write(json_object)
        
        
    def trustedCommands(self):       
        @bot.command()
        async def bindserver(message, server):
            self.readJson('servers.json')
            if message.author.id in self.trusted:               
                bindEmbed = discord.Embed(color=0xFF99E5)
                server = bot.get_guild(int(server))
                bindEmbed.set_author(name='Action: Server binded to channel')
                bindEmbed.add_field(name='server: {}'.format(server), value='binded to <#{}>'.format(message.channel.id), inline=True)
                await message.channel.send(embed=bindEmbed) 
                masterDict = {int(server) : message.channel.id}
                self.writeJson(masterDict, 'servers.json')
                
                
        @bot.command()
        async def displayactive(message):
            if message.author.id in self.trusted:
                self.readJson('servers.json')
                self.displayActive = discord.Embed(color=0xBD5CFF)
                self.displayActive.set_author(name="Servers being Tracked".format(message.guild, message.guild.id),
                icon_url='https://cdn.discordapp.com/attachments/748479776666419223/749449403080900698/chillstolfo.png')
                for i in self.jsonDict:
                    displayGuild = bot.get_guild(int(i))
                    self.displayActive.add_field(name='Server: {}'.format(displayGuild), value='channel: <#{}>'.format(self.jsonDict[i]), inline=True)
                    
                await message.channel.send(embed=self.displayActive)
                
        @bot.command()
        async def displayannoy(message):
            if message.author.id in self.trusted:
                annoyEmbed = discord.Embed(title='Victims being annoyed:', color=0xE5FF99)
                for i in self.annoyList:
                    annoyEmbed.add_field(name='Victim:', value='<@{}>'.format(i), inline=True)
                await message.channel.send(embed=annoyEmbed)
        
        @bot.command()
        async def annoy(message, user):
            if message.author.id in self.trusted:
                self.mentionOrID(user)
                
                annoyEmbed = discord.Embed(color=0x99FFE5, title="Annoying User")
                
                if self.ID in self.annoyList:
                    self.annoyList.remove(self.ID)
                    annoyEmbed.add_field(name='User Removed', value='user <@{}> removed from annoyList'.format(self.ID), inline=True)
                elif self.ID not in self.annoyList:
                    self.annoyList.append(self.ID)
                    annoyEmbed.add_field(name='User Added', value='user <@{}> added to annoyList'.format(self.ID), inline=True)
                
                await message.send(embed=annoyEmbed)
                
                
        
        @bot.command()
        async def award(message, arg, points):
            if message.author.id in self.trusted:
                allowedList = ['1','2','3','4','5','6','7','8','9','0']
                allowed = 0
                
                self.readJson('points.json')
                self.mentionOrID(arg)
                
                for i in points:
                    if i not in allowedList:
                        allowed += 1
                    else:
                        allowed += 0
                
                if allowed == 0:
                    pointEmbed = discord.Embed(color=0xACB5FF)
                    pointEmbed.set_author(name='Action: Awarded points')
                    if self.ID not in self.jsonDict:

                        tempDict = {self.ID:int(points)}
                        self.writeJson(tempDict, 'points.json')
                        
                        pointEmbed.add_field(name='Point Logs:', value='User <@{}> was awarded {} points, now they have {} points.'.format(self.ID, points, points), inline=True)
                        
                        await message.channel.send(embed=pointEmbed)
                        
                    else:
                        oldPoints = self.jsonDict.pop(self.ID)
                        newPoints = int(points)
                        
                        newValue = oldPoints + newPoints
                        tempDict = {self.ID : newValue}    

                        self.writeJson(tempDict, 'points.json')
                        
                        pointEmbed.add_field(name='Point Logs:', value='User <@{}> was awarded {} points, now they have {} points.'.format(self.ID, points, newValue), inline=True)
                        
                        await message.channel.send(embed=pointEmbed)
                        
                else:
                    pointEmbed = discord.Embed(color=0xACB5FF, name='Exception Passed')
                    pointEmbed.add_field(name='ValueError:', value="Expected int instead of {}".format(type(points)))
                    
                    await message.channel.send(embed=pointEmbed)
        
        @bot.command()
        async def deduct(message, arg, points):
            if message.author.id in self.trusted:
                allowedList = ['1','2','3','4','5','6','7','8','9','0']
                allowed = 0
                
                self.readJson('points.json')
                self.mentionOrID(arg)
                
                for i in points:
                    if i not in allowedList:
                        allowed += 1
                    else:
                        allowed += 0
                
                if allowed == 0:
                    pointEmbed = discord.Embed(color=0xACB5FF, name='User Deducted ~~good boy~~ points')
                    pointEmbed.set_author(name='Action: Deducted points')
                    if self.ID not in self.jsonDict:
                        
                        newPoints = points * -1
                        tempDict = {self.ID:int(newPoints)}
                        self.writeJson(tempDict, 'points.json')
                        
                        pointEmbed.add_field(name='Point Logs:', value='user <@{}> was deducted {} points, now they have {} points.'.format(self.ID, points, newPoints), inline=True)
                        
                        await message.channel.send(embed=pointEmbed)
                        
                    else:
                        oldPoints = self.jsonDict.pop(self.ID)
                        newPoints = int(points) * -1
                        
                        newValue = oldPoints + newPoints
                        tempDict = {self.ID : newValue}    

                        self.writeJson(tempDict, 'points.json')
                        
                        pointEmbed.add_field(name='Point Logs:', value='user <@{}> was deducted {} points, now they have {} points.'.format(self.ID, points, newValue), inline=True)
                        
                        await message.channel.send(embed=pointEmbed)
                        
                else:
                    pointEmbed = discord.Embed(color=0xACB5FF, name='Exception Passed')
                    pointEmbed.add_field(name='ValueError:', value="Expected int instead of {}".format(type(points)))
                    
                    await message.channel.send(embed=pointEmbed)
        
        
    def adminCommands(self):
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
            self.mentionOrID(arg)
                        
            kickVictim = await bot.fetch_user(self.ID)
            
            
            kickEmbed = discord.Embed(color=0xFFBDBD)
            kickEmbed.set_author(name='action: User Kicked')

            if args == ():
                kickEmbed.add_field(name='conducted by {}'.format(message.author), value='<@{}> has been kicked'.format(self.ID), inline=True)
                await message.guild.kick(kickVictim, reason='conducted by {}'.format(message.author))
            else:
                kickReason = ''
                for i in args:
                    kickReason = kickReason + ' ' + i
                kickEmbed.add_field(name='conducted by {}'.format(message.author), value='<@{}> has been kicked for {}'.format(self.ID, kickReason), inline=True)
                
                await message.guild.kick(kickVictim, reason=kickReason+' conducted by {}'.format(message.author))
            await message.send(embed=kickEmbed)
            
        @bot.command()
        @commands.has_permissions(ban_members=True)
        async def ban(message, arg, days='0', *args, **kwargs):

            self.mentionOrID(arg)
            banVictim = await bot.fetch_user(self.ID)
            banEmbed = discord.Embed(color=0xFFBDBD)
            banEmbed.set_author(name='action: User banned')
            allowedList = ['1','2','3','4','5','6','7','8','9','0']
            allowed = 0
            
            def noReason():
                banEmbed.add_field(name='conducted by {}'.format(message.author), value='<@{}> has been banned (messages deleted in days: {})'.format(self.ID, days), inline=True)
                
                
            def withReason():
                self.banReason = ''
                for i in args:
                    self.banReason = self.banReason + ' ' + i
                banEmbed.add_field(name='conducted by {}'.format(message.author), value='<@{}> has been banned for {} (messages deleted in days: {})'.format(self.ID, self.banReason, days), inline=True)
            
            for i in days:
                if i not in allowedList:
                    allowed += 1
                else:
                    allowed += 0
                    
            if allowed == 0:
                intDays = int(days)
                test = isinstance(intDays, int)
                
                
                #with everything
                if args != ():
                    withReason()
                    await message.guild.ban(banVictim, delete_message_days=days, reason=self.banReason) 
                #with days
                elif test == True:
                    noReason()
                    await message.guild.ban(banVictim, delete_message_days=days)
                #with nothing
                else:
                    await message.guild.ban(banVictim, delete_message_days=days) 
            else:
                if allowed != 0:
                    days = 0
                    error = 'tl;dr, the correct format is ;ban (userID/mention) (days) (reason). You passed reason without passing days so it defaulted to 0 days and banned wihtout a reason. Use the correct formatting next time >:|'
                    banEmbed.add_field(name='conducted by {}'.format(message.author), value='<@{}> has been banned'.format(self.ID), inline=True)
                    banEmbed.set_footer(text=error)
                    await message.guild.ban(banVictim, delete_message_days=days) 

            await message.send(embed=banEmbed)
            
            
    def userCommands(self):
        @bot.command()
        async def ping(message):
            await message.channel.send('pong!')
        
        @bot.command()
        async def help(message):
            helpOwner = discord.Embed(color=0xCAFFFF, title="Bot Commands")
            helpOwner.set_author(name='Help has arrived :D',
            icon_url='https://cdn.discordapp.com/attachments/748479776666419223/749449403080900698/chillstolfo.png')
            
            helpOwner.add_field(name=";bindserver (server ID)", value='binds all messages from that server to be redirected to this channel (needs bot inside that server)', inline=True)
            helpOwner.add_field(name=';displayactive', value='displays all active servers', inline=True)
            helpOwner.add_field(name=';annoy (targetID/mention)', value='you get annoyed. Idiot', inline=True)
            helpOwner.add_field(name=';displayannoy', value='shows all victims of harassment', inline=True)
            helpOwner.add_field(name=';award (targetID) (points)', value='gives good boy points', inline=True)
            helpOwner.add_field(name=';deduct (targetID) (points)', value='takes away good boy points', inline=True)
            helpOwner.set_footer(text="this only exists because I don't comment my code :c (check out my github)")
            
            await message.channel.send(embed=helpOwner)
            
            helpAdmin = discord.Embed(color=0xFFFFCA, title="Admin Commands")
            helpAdmin.add_field(name=';clear (x)', value='clears x amount of messages in chat', inline=True )
            helpAdmin.add_field(name=';kick (targetID/mention) (reason)', value='kicks a member using their ID or mentioning them. Duh. (reason is optional)', inline=True )
            helpAdmin.add_field(name=';ban (targetID/mention) (days) (reason)', value='bans a user using their ID or mentioning them. Duh. (days and reason are optional)', inline=True )
            helpAdmin.set_footer(text="this only exists because I don't comment my code :c (check out my github)")
            
            await message.channel.send(embed=helpAdmin)
            
            helpUser = discord.Embed(color=0xBDFFBD, title='User Commands')
            helpUser.add_field(name=";help", value='prints out this menu', inline=True)
            helpUser.add_field(name=";ping", value='pong?', inline=True )
            helpUser.add_field(name=";embedthis (title) (body)", value='takes your mortal loser message and converts it into an embed (useless, I know)', inline=True )
            helpUser.add_field(name=";points (targetID/mention)", value='displays how much ~~good boy~~ points the user has ', inline=True )
            helpUser.set_footer(text="this only exists because I don't comment my code :c (check out my github)")
            
            await message.channel.send(embed=helpUser)
            
            moreInfo = discord.Embed(title='https://github.com/megumin00/authoritarian-dictatorship-discbot')
            
            await message.channel.send(embed=moreInfo)
            
        @bot.command()
        async def embedthis(message, title, *args):
            user = message.guild.get_member(message.author.id)
            pfp = user.avatar_url
            embedList = ''
            for i in args:
                embedList = embedList + ' ' + i
                
            embedSend = discord.Embed(color=0xBDBDFF)
            embedSend.set_author(name='Embed requested from {}'.format(message.author),
            icon_url=str(pfp))
            embedSend.add_field(name=title, value=embedList)
            
            await message.channel.send(embed=embedSend)
            
        @bot.command()
        async def points(message, arg):
            self.readJson('points.json')
            self.mentionOrID(arg)
            
            displayPoints = discord.Embed(color=0xFFE3AC)
            displayPoints.add_field(name='Current Points:', value='<@{}> currently has {} good boy points'.format(self.ID, self.jsonDict.get(str(self.ID))))
            
            await message.channel.send(embed=displayPoints)
            
    def serverLog(self): 
        @bot.event
        async def on_message(message):
            if message.author != bot.user:
                self.readJson('servers.json')
                if str(message.guild.id) in self.jsonDict:
                    loggedChannel = self.jsonDict.get(str(message.guild.id))
                    loggedChannelGet = bot.get_channel(loggedChannel)
                        
                    embedVar = discord.Embed(title="{}".format(message.content), color=0xFFCAFF)
                    embedVar.set_author(name="Message sent in {}, (ID:{})".format(message.guild, message.guild.id),
                    icon_url='https://cdn.discordapp.com/attachments/748479776666419223/749449403080900698/chillstolfo.png')
                    embedVar.add_field(name="Channel: {}, (ID:{})".format(message.channel, message.channel.id), value='by <@!{}>, <#{}> (ID:{})'.format(message.author.id, message.channel.id, message.author.id), inline=True)
    
                    await loggedChannelGet.send(embed=embedVar)
                
                if str(message.author.id) in self.annoyList:
                    pick = [True, False]
                    totalString = ''
                    for i in message.content:
                        TrueFalse = random.choice(pick)
                        if TrueFalse == True:
                            totalString += i.capitalize()
                        else:
                            totalString += i.lower()
                    await message.channel.send(totalString)
                        
                        
                await bot.process_commands(message)
                    
        
        @bot.listen("on_command_error")
        async def on_command_error(message, error):        
            error = error.__cause__ or error
            if isinstance(error, commands.CommandNotFound):
                return
            
            await message.send(error)
            
    def run(self):
        self.trustedCommands()
        self.adminCommands()
        self.userCommands()
        self.serverLog()
        
        bot.run('')
        
    

if __name__ == "__main__":
    bot = commands.Bot(command_prefix=';')
    bot.remove_command('help')
    nest_asyncio.apply()
    
    
    discBot = discBot()
    discBot.run()
