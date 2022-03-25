from discord import Embed, Color

'''
Drink Object
    Processes json data retrieved from the request object and
    stores a Discord.Embed object
'''
class Drink():
    def __init__(self, drink_json: dict):
        drink_json = self.sanitize_json(drink_json)
        self.img = drink_json.get('strDrinkThumb')
        self.name = drink_json.get('strDrink')
        self.category = drink_json.get('strCategory')
        self.alcoholic = drink_json.get('strAlcoholic')
        self.glass = drink_json.get('strGlass')
        self.ingredients_string = self.get_ingredient_string(drink_json)
        self.instructions = drink_json.get('strInstructions')
        self.embed = self.embed_drink()

    
    def sanitize_json(self, json: dict):
        drink_dict = {}
        for key in json:
            if(json[key] != None):
                drink_dict[key] = json[key]  

        return drink_dict  
    
    
    def get_ingredient_string(self, json) -> list:
        ingredients = [json.get(ing) for ing in json if 'Ingredient' in ing and json.get(ing) is not None]
        measurements = [json.get(measure) for measure in json if 'Measure' in measure and json.get(measure) is not None]
        
        if(len(measurements) == 0):
            return ingredients
        
        ingredient_list = []
        for i in range(len(ingredients)):
            if(i < len(measurements)):
                ingredient_list.append(measurements[i].strip() + " " + ingredients[i])
            elif(ingredients[i] == ' '):
                pass
            else:
                ingredient_list.append(ingredients[i])
        return ingredient_list

    def embed_drink(self) -> Embed:
        embed = Embed(title= self.name, description='A drink for you, good Bud.', color=Color.dark_blue().value)
        embed.set_image(url= self.img)
        embed.add_field(name="Name", value= self.name)
        embed.add_field(name="Category", value= self.category)
        embed.add_field(name="\u200b", value='\u200b')
        embed.add_field(name="Alcoholic?", value= self.alcoholic)
        embed.add_field(name="Glass Type", value= self.glass)
        embed.add_field(name="\u200b", value='\u200b')
        ingredient_string = ""
        for string in  self.ingredients_string:
            ingredient_string += string + '\n'
        embed.add_field(name="Ingredients", value=ingredient_string, inline=False)
        embed.add_field(name="Instructions", value= self.instructions, inline=False)
        embed.set_footer(text="Have ideas for additional functionality? Throw them in #robbot_discussion!")
        return embed