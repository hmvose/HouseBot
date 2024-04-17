#bot.py

#importing important and necessary files
import os
import logging

#importing non-native files
import discord
from dotenv import load_dotenv
from discord.utils import get
from discord import Intents
from discord.ext import tasks

#logging the discord bot startup
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#gets the intents library in order to use on_raw_reaction commands
intents = discord.Intents.all()
client = discord.Client(intents = intents)

load_dotenv('test.env')
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#generates the automated messages and establishes the time between each message
#this has to come first since the test.start() function requires the on_ready() event
#which also happens to take care of all of the bot connection logging in the window so yeehaw
@tasks.loop(minutes = 60)
async def test():
    channel = client.get_channel(1090789895557099590) #gets the channel to send the message in
    colorStr = str("```diff\n-ahahaha guess who isn't dead fuckers (although i'll probably be repurposing some stuff for the sake of not getting burnt out every time i look at my code)\n```") #groups all text into a single string (note: diff and the - means red text)
    await channel.send(colorStr) #generates the message

#basically handles any immediate bot interaction with the server
#automated messages and recognizing when the established connection is created
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!') #sends a message when the bot has connected

    #making sure we're dealing with the right server
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    #prints the guild members in a list
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

    #initiates the automated message timer/sequence
    #test.start()

test_user = ['one', 'two']

# This sends an embed message with a description of the roles.
# These are the prompts for each floor/area. Some may have specific descriptors for emojis, others
# may only have a clue to hint at which emoji the user should use.

@client.event
async def on_message(message):

    global updateID

    #to make this a full system, make a dictionary where key = user ID and element = inventory list
    #would rely on specific naming to add and remove but i think it could totally work, need to have a check/init option
    #gets info for specific user sends: inventory listing from a given list (could make an embed but i'm lazy as hell)
    channel = client.get_channel(1090789895557099590)
    if message.content == 'inventory':
        if message.author.id == 418628513646641153:
            start_sentence = ' '
            for x in test_user:
                start_sentence += '\n' + '-' + x
            message = await channel.send(start_sentence)

    #login entry message - UPDATED
    if message.channel.id == 1090789895557099590:
        def enterMessage():
            enterMessage.embedvar = discord.Embed(title="You have been invited inside.",
                                    description="React with the key to enter the mansion.\n:key:"
                                                " - Mansion Key\n", color=0x00ff00)
            #embedvar.add_field(name="newInvite", value="sure", inline=True) this adds extra stuff
        if message.content == "enter": #checks the user message to see if they would like to summon the bot
            enterMessage()
            message = await message.channel.send(embed=enterMessage.embedvar)
            #global updateID
            updateID = message.id
        
    #entrance channel elevator message
    elif message.channel.id == 796961217885372446: #maybe make an elevator?

        #message to go up to second floor
        def enterMessageFloor2():
            enterMessageFloor2.embedvar = discord.Embed(title="You are standing in front of the stairs.",
                                      description="React with :arrow_up: to climb the stairs.", color=0x00ff00)
        #message to go up to third floor
        def enterMessageFloor3():
            enterMessageFloor3.embedvar = discord.Embed(title="You are standing in front of the stairs.",
                                      description="React with :arrow_up: to climb the stairs.", color=0x00ff00)

        #message to go up to fourth floor
        def enterMessageFloor4():
            enterMessageFloor4.embedvar = discord.Embed(title="You are standing in front of the stairs.",
                                      description="React with :arrow_up: to climb the stairs.", color=0x00ff00)

        #message to go to basement
        def enterMessageDown():
            enterMessageDown.embedvar = discord.Embed(title="On the first landing, a small door opens to reveal an elevator.",
                                      description="React with :arrow_double_down: to go to the basement.", color=0x00ff00)

        #key words
        if message.content == 'stair':
            enterMessageFloor2()
            message = await message.channel.send(embed=enterMessageUp.embedvar) #CHECK enterMessageUp
            global updateIDUp
            updateIDUp = message.id
        elif message.content.startswith('basement'):
            enterMessageDown()
            message = await message.channel.send(embed=enterMessageDown.embedvar)
            global updateIDDown
            updateIDDown = message.id
        elif message.content.startswith('examine.'):
            examineEvidence()
            message = await message.channel.send(embed=examineEvidence.embedvar)

    elif message.channel.id == 796961447216807936: #foyer channel
        def stairDown():
            stairDown.embedvar = discord.Embed(title="You are standing in front of the stairs.",
                               description="React with :arrow_down: to descend the stairs.", color=0x00ff00)
        if message.content.startswith('stair'):
            stairDown()
            message = await message.channel.send(embed=stairDown.embedvar)
            global updateIDDescend
            updateIDDescend = message.id

    elif message.channel.id == 796961113601998859: #sunroom channel
        def outMessage():
            outMessage.embedvar = discord.Embed(title="There is a door leading to the patio area.",
                                description="React with :sunny: to go outside.", color=0x00ff00)
        if message.content.startswith('outside'):
            outMessage()
            message = await message.channel.send(embed=outMessage.embedvar)
            global updateIDOut
            updateIDOut = message.id

    elif message.channel.id == 807013393906794536: #patio channel
        def inMessage():
            inMessage.embedvar = discord.Embed(title="There is a door leading into the sunroom.",
                               description="React with :house: to go inside.", color=0x00ff00)
        if message.content.startswith('inside'):
            inMessage()
            message = await message.channel.send(embed=inMessage.embedvar)
            global updateIDIn
            updateIDIn = message.id
        
    elif message.channel.id == 807015252365410317: #atrium channel
        def a2eMessage():
            a2eMessage.embedvar = discord.Embed(title="You call the elevator, and the door slowly opens.",
                                description="React with :arrow_double_up: to return to the first floor.", color=0x00ff00)
        if message.content.startswith('entrance'):
            a2eMessage()
            message = await message.channel.send(embed=a2eMessage.embedvar)
            global updateIDa2e
            updateIDa2e = message.id
            
    #MESSAGE ONLY COMMANDS; NO ROLE ASSIGNMENT ASSOCIATED

    elif message.channel.id == 797290243832938537: #theatre channel

        evidenceDescription = "Looking around, you notice two things. \n" \
        "1. There is a spot in the carpet just in front of the overhang of the mezzanine that appears to be stained. It is an unidentifiable fluid, but it appears semi-recent. \n" \
        "2. Although there are signs of wear on all of the handrails in the mezzanine, one in particular is noticeably dented on one side. It is about the size of a tennis ball." 
        
        def closetOpen():
            closetOpen.embedvar = discord.Embed(title="You take a step back as the wall panel swings open.",
                                description="A small closet stands before you. In it, is: \n"
                                "-A small vacuum, with several dried red blots on the handle \n"
                                "-A mop, with a head that appears to be tainted pink \n"
                                "-A large shelf with various tools, though one wrench in particular seems to be missing. \n"
                                "After a short period of time, the door closes on its own.", color=0x00ff00)
        
        if message.content.startswith('knock knock knock.'): #checks for correct amount of knocks
                closetOpen()
                message = await message.channel.send(embed=closetOpen.embedvar)
        elif message.content.startswith("$examine"):
            examineEvidence()
            message = await message.channel.send(embed=examineEvidence.embedvar)
            
    else:
        return


@client.event
async def on_raw_reaction_add(payload):

    guild = client.get_guild(payload.guild_id)
    member = get(guild.members, id = payload.user_id)
  
    if payload.channel_id == 1090789895557099590: #front-gates channel
        if payload.emoji.name == "🔑" and payload.message_id == updateID:
            role = discord.utils.get(guild.roles, name="MANSION - FIRST FLOOR")
            await payload.member.add_roles(role)
            
    elif payload.channel_id == 796961217885372446: #entrance channel
        if payload.emoji.name == "⬆️" and payload.message_id == updateIDUp:
            role = discord.utils.get(guild.roles, name="Mansion - Second Floor")
            await payload.member.add_roles(role)
            badrole = discord.utils.get(guild.roles, name="Mansion - First Floor")
            await payload.member.remove_roles(badrole)

        elif payload.emoji.name == "⬇️" and payload.message_id == updateIDDown:
            role = discord.utils.get(guild.roles, name="Mansion - Basement")
            await payload.member.add_roles(role)
            badrole = discord.utils.get(guild.roles, name="Mansion - First Floor")
            await payload.member.remove_roles(badrole)

    elif payload.channel_id == 796961447216807936: #foyer channel
        if payload.emoji.name == "⏬" and payload.message_id == updateIDDescend:
            role = discord.utils.get(guild.roles, name="Mansion - First Floor")
            await payload.member.add_roles(role)
            badrole = discord.utils.get(guild.roles, name="Mansion - Second Floor")
            await payload.member.remove_roles(badrole)

    elif payload.channel_id == 796961113601998859: #sunroom channel
        if payload.emoji.name == "☀️" and payload.message_id == updateIDOut:
            role = discord.utils.get(guild.roles, name="Mansion - Backyard")
            await payload.member.add_roles(role)
            badrole = discord.utils.get(guild.roles, name="Mansion - First Floor")
            await payload.member.remove_roles(badrole)

    elif payload.channel_id == 807013393906794536: #patio channel
        if payload.emoji.name == "🏠" and payload.message_id == updateIDIn:
            role = discord.utils.get(guild.roles, name="Mansion - First Floor")
            await payload.member.add_roles(role)
            badrole = discord.utils.get(guild.roles, name="Mansion - Backyard")
            await payload.member.remove_roles(badrole)

    elif payload.channel_id ==  807015252365410317: #atrium channel
        if payload.emoji.name == "⏫" and payload.message_id == updateIDa2e:
            role = discord.utils.get(guild.roles, name="Mansion - First Floor")
            await payload.member.add_roles(role)
            badrole = discord.utils.get(guild.roles, name="Mansion - Basement")
            await payload.member.remove_roles(badrole)

    else:
        return


client.run(TOKEN)