import os
import discord
from requests.api import get
from util import Bartender
from util.Pin import Pin
from dotenv import load_dotenv

SHEBANGS = '.!$'

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    await check_react_ohwow(message)

    if not should_respond_msg(message):
        return

    cmd = get_msg_cmd(message)

    if cmd == '8ball':
        pass
    if cmd == 'roll':
        pass
    if cmd == 'bg':
        await message.channel.send('hey')
    if cmd == 'drink' or cmd == 'cocktail':
        await get_cocktail(message)
    if cmd == 'pin':
        await pin_message(message)
    
    return



def should_respond_msg(msg) -> bool:
    if msg.author == client.user:  # Robbot is the author
        return False
    if msg.content[0] not in SHEBANGS:
        return False
    return True

def get_msg_cmd(msg):
    content = msg.content[1:]
    parts = content.split()
    cmd = parts[0].lower()  # TODO check parts nonempty

    return cmd

async def check_react_ohwow(message):
    if 'oh wow' in message.content.lower():
        for emoji in client.emojis:
            if emoji.name == 'ohwow':
                await message.add_reaction(emoji)

'''
@author: Keeth S.
@dependencies: util/Bartender.py
@desc: Returns a random drink embedded from the Drink object's  embed method
@retunrs: async message back to channel
# TODO Optimize Drink Object.
'''
async def get_cocktail(msg):
    try:
        
        await msg.channel.send(embed=Bartender.get_drink().embed())
    except Exception as ex:
        print(ex)
        await msg.channel.send('Ayo, your code is wack.')

'''
@author: Keeth S.
@dependencies: util/Pin.py
@desc: Sends a embed to the Pin channel when a user reply's to a message with .pin
@retunrs: async message back to channel confirming message was pinned
# TODO Optimize Drink Object.
'''
async def pin_message(msg):
    try:
        if not msg.reference:
            await msg.channel.send('Sorry, bud. Just can\'t do it.')
            return
        reply = await msg.channel.fetch_message(msg.reference.message_id)
        pin_embed = Pin(reply)
        pin_channel = client.get_channel(789771971532947486)
        await pin_channel.send(embed=pin_embed.embed())
        await msg.channel.send('You got it, bud.')
    except Exception as ex:
        print(ex)
        await msg.channel.send('Ayo, your code is wack.')

client.run(TOKEN)