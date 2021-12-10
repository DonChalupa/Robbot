from abc import ABC, abstractmethod
from discord import Embed
from util.Utility import Colors
#region Embedder
'''
@author: Keeth S.
@params: filth: Object which needs to be sanitized
@desc: Parent Sanitizer Class
'''
class Embedder(ABC):
    
    @abstractmethod
    def embed(filth):
        ''' Cleans the incoming filth data for the given sanitizer object '''
'''
@author: Keeth S.
@params: drink: Drink object to be embedded
@desc: Embedder which creates and sets an embed with
        information from the Drink object
'''
class DrinkEmbedder(Embeder):
    
    @staticmethod
    def embed(self, drink):

        embed = Embed(title= drink._name, description='A drink for you, good Bud.', color=Colors().dark_navy)
        embed.set_image(url= drink._img)
        embed.add_field(name="Name", value= drink._name)
        embed.add_field(name="Category", value= drink._category)
        embed.add_field(name="\u200b", value='\u200b')
        embed.add_field(name="Alcoholic?", value= drink._alcoholic)
        embed.add_field(name="Glass Type", value= drink._glass)
        embed.add_field(name="\u200b", value='\u200b')
        ingredient_string = ""
        for string in  drink._ingredients_string:
            ingredient_string += string + '\n'
        embed.add_field(name="Ingredients", value=ingredient_string, inline=False)
        embed.add_field(name="Instructions", value= drink._instructions, inline=False)
        embed.set_footer(text="Have ideas for additional functionality? Throw them in #robbot_discussion!")
        return embed


'''
@author: Keeth S.
@params: pin: Pin object to be embedded
@desc: Embedder which creates and sets an embed with
        information from the Pin object
'''
class PinEmbedder(Embedder):

    @staticmethod
    def embed(self, pin):
        embed = Embed(title=pin.author, description=f'Posted on {pin.posted_date}', color=int(Colors().user_colors.get_user_color(pin.id)))
        pin_embed = embed
        pin_embed.set_thumbnail(url=pin.avatar)
        pin_embed.add_field(name="Channel", value=pin.channel, inline=False)
        if(pin.image is not None):
            pin_embed.set_image(url=pin.image)
        if(pin.content is not None):
            pin_embed.add_field(name="Message", value=f'[{pin.content}]({pin.url})', inline=False)
        else:
            pin_embed.add_field(name="Message", value='*This pin had no message*', inline=False)
        return pin_embed

class EmbedderFactory:
    embedders = {
        "drink": DrinkEmbedder,
        "pin": PinEmbedder
    }
    
    @staticmethod
    def get_sanitizer(type: str):
        if type in EmbedderFactory.embedders:
            return EmbedderFactory.embedders[type]()
        else:
            raise KeyError('Not a valid Embedder Type')
#endregion