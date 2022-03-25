import traceback
import requests as req
from discord.ext import commands
from models.Drink import Drink

class Bartender(commands.Cog, name='Bartender', description='Used to provide any bud with a delicious, sensual drink.'):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='drink', description='Get a nice, refreshing drink from the Bartender', usage='[A (Alchoholic) || NA (Nonalcoholic)]')
    async def drink(self, ctx, *args):
        DRINK_URL = 'https://www.thecocktaildb.com/api/json/v1/1/random.php'
        try:
            json = req.get(DRINK_URL).json()['drinks'][0]

            if not args:
                drink = Drink(json)
                await ctx.send(embed = drink.embed)

            else:
                await ctx.send('Awaiting Logic...')
            
        except Exception as ex:
            traceback.print_exc()
            await ctx.send(f'Ayo, your code is wack.\n Error: {ex}')

def setup(bot):
    bot.add_cog(Bartender(bot))
