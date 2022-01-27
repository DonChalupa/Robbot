import os
import json
import random
import re
import requests
import asyncio
import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv

from funcs.Bartender import Drink
from funcs.Pin import Pin
from util.Request import Request
from util.Sanitizer import DrinkJsonSanitizer
from util.Formatter import DrinkFormatter
from util.Embedder import DrinkEmbedder, PinEmbedder
from util import Rolls
from util.Music import Music

CFG_FILENAME = 'config.json'
request = Request(requests)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

with open(CFG_FILENAME) as cfg:
    CFG = json.load(cfg)


bot = commands.Bot(command_prefix=commands.when_mentioned_or('.'))

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    await check_react_ohwow(message)

    await bot.process_commands(message)
    return

@bot.command(name='8ball')
async def shake_8ball(ctx):
    async with ctx.typing():
        responses = CFG['8ball_responses']
        response = random.choice(responses)

    await ctx.send(response, tts=True)

@bot.command(name='roll')
async def roll(ctx, *args):
    async with ctx.typing():
        args_as_str = ' '.join(args)
        roll = Rolls.rolls_from_args(args_as_str)

    await ctx.send(roll, tts=True)

# Voice / Music
@bot.command()
async def join(ctx, *, channel: discord.VoiceChannel):
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)
    await channel.connect()

@bot.command()
async def play(ctx, *, url):
    async with ctx.typing():
        player = await Music.YTDLSource.from_url(url, loop=bot.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

    await ctx.send(f'Now playing: {player.title}')

@bot.command()
async def stop(ctx):
    async with ctx.typing():
        await asyncio.sleep(0)
    await ctx.send(r'Okay... :(')

    await ctx.voice_client.disconnect()

@play.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        channel = _get_voice_channel_to_join(ctx)
        await channel.connect()
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()

def _get_voice_channel_to_join(ctx):
    if ctx.author.voice:
        return ctx.author.voice.channel
    else:
        return _get_most_populated_voice_channel(ctx)

def _get_most_populated_voice_channel(ctx):
    voice_channels_reverse_order = ctx.guild.voice_channels[::-1]
    channel_populations = {len(channel.members) : channel for channel in voice_channels_reverse_order}
    max_population = max(channel_populations.keys())
    channel = channel_populations[max_population]
    return channel
        

@bot.command(name='downloadMsgs')
async def download_msgs(ctx):
    if 'Patriarch' in [role.name for role in ctx.author.roles]:
        await _download_msgs(ctx)
    else:
        await ctx.send('pls no')

async def _download_msgs(ctx):
    #open write file
    #setup json
    #get messages
    ROBBOT_ID = 422470851435298818
    async with ctx.typing():
        # create filename
        date = datetime.datetime.now().strftime("%w%d%YT%H%M%S")
        filename = f'messages_{date}.json'
        # get data directory
        script_dir = os.path.dirname(__file__)
        guild_name = "".join(x for x in ctx.guild.name if x.isalnum())  # need to sanitize ':', etc
        data_dir = os.path.join(script_dir, f"data/{guild_name}_{ctx.guild.id}/{filename}")
        data_dir = os.path.abspath(data_dir)
        
        with open(filename, 'w+') as f:
            messages = {}
            channels = ctx.guild.text_channels
            messages['messages'] = []
            for channel in channels:
                if ROBBOT_ID in [member.id for member in channel.members]:
                    discord_msgs = await channel.history(limit=None).flatten()
                    for discord_msg in discord_msgs:
                        if discord_msg.author.id != ROBBOT_ID:  # TODO fix magic number (robbots ID)
                            messages['messages'].append({'author_id': discord_msg.author.id,
                                                        'content': discord_msg.content})
            json.dump(messages, f)
        await ctx.send('Done')



@bot.command()
async def test(ctx):
    await ctx.send('.test')

async def check_react_ohwow(message):
    if 'oh wow' in message.content.lower():
        for emoji in bot.emojis:
            if emoji.name == 'ohwow':
                await message.add_reaction(emoji)


'''
@author: Keeth S.
@desc: Returns a random drink embedded from the Drink object's  embed method
@retunrs: async message back to channel
'''
@bot.command()
async def drink(ctx):
    try:
        drink_json = request.get_drink_json()
        drink = Drink(drink_json, DrinkJsonSanitizer, DrinkFormatter, DrinkEmbedder)
        await ctx.send(embed = drink.embed)
    except Exception as ex:
        print(ex)
        await ctx.send('Ayo, your code is wack.')

@bot.command()
async def cocktail(ctx):
    await drink(ctx)

'''
@author: Keeth S.
@desc: Sends a embed to the Pin channel when a user reply's to a message with .pin
@retunrs: async message back to channel confirming message was pinned
'''
@bot.command()
async def pin(ctx):
    try:
        if not ctx.message.reference:
            await ctx.message.channel.send('You have to reply .pin to the message you want pinned.')
            return
        reply = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
        pin = Pin(reply, PinEmbedder)
        pin_channel = bot.get_channel(789771971532947486)
        await pin_channel.send(embed=pin.embed)
        await ctx.message.channel.send('You got it, bud.')
    except Exception as ex:
        print(ex)
        await ctx.message.channel.send('Ayo, your code is wack.')


async def get_cocktail(msg):

    pass

bot.run(TOKEN)