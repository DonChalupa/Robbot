import traceback
import requests as req
import random as r
from discord.ext import commands
from models.Drink import Drink

BARTENDER_DESCRIPTION = 'Used to provide any bud with a delicious, sensual drink.'
DRINK_DESCRIPTION = 'Get a nice, refreshing drink from the Bartender'
DRINK_USAGE = '--> Gets a random drink\n.drink a --> Gets an alcoholic drink\n.drink na --> gets a nonalcoholic drink\n.drink [bourbon,brandy,cognac,gin,rum,scotch,tequila,vodka,whiskey,wine] --> Gets an alcoholic beverage of the given type'
class Bartender(commands.Cog, name='Bartender', description=BARTENDER_DESCRIPTION):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='drink', description=DRINK_DESCRIPTION, usage=DRINK_USAGE)
    async def drink(self, ctx, *args):
        FILTER_TYPES = ['a','bourbon','brandy','cognac','gin', 'na','rum','scotch','tequila','vodka','whiskey','wine']
        drink_url = 'https://www.thecocktaildb.com/api/json/v1/1/'

        try:
            if not args:
                drink_url += 'random.php'
                json = req.get(drink_url).json()
                drink = Drink(json['drinks'][0])
                await ctx.send(embed = drink.embed)
                return
            

            if len(args) > 1:
                await ctx.send(f'I think you added too many arguments there, bud.')
                return

            arg = args[0].lower()
            if arg not in FILTER_TYPES:
                    message = 'Better check your arguments there, bud.'
                    chance = r.randint(1,100)
                    if chance > 80:
                        message += ' (Kinda cringe...)'
                    await ctx.send(message)
                    return
            
            
            if arg == 'a':
                filter = 'filter.php?a=Alcoholic' 
                resolved_url = self.drink_url_factorty(drink_url, filter)
            elif arg == 'na':
                filter = 'filter.php?a=Non_Alcoholic'
                resolved_url = self.drink_url_factorty(drink_url, filter)
            else:
                filter = f'filter.php?i={arg}'
                resolved_url = self.drink_url_factorty(drink_url, filter)
            
            json = req.get(resolved_url).json()
            drink = Drink(json['drinks'][0])
            await ctx.send(embed = drink.embed)

        except Exception as ex:
            traceback.print_exc()
            await ctx.send(f'Ayo, your code is wack.\n Error: {ex}')


    def drink_url_factorty(self, drink_url, filter):
        filter_url = drink_url + filter
        drink_list = req.get(filter_url).json()['drinks']
        drink_id = r.choice(drink_list)['idDrink']

        return drink_url + f'lookup.php?i={drink_id}'


def setup(bot):
    bot.add_cog(Bartender(bot))
