import pandas as pd
import random
import joblib

class NutritionFacts():
    def __init__(self, nutrientsLink):
        self.nutrDf = pd.read_csv(nutrientsLink, index_col=0)
        
    def getNutrients(self, product):
        try:
            nutr = self.nutrDf.loc[product]
            return nutr
        except Exception:
            print(f"failed to find an ingridient {product}")
            return None
        
    
    def printNutrients(self, product):
        nutr = self.getNutrients(product)
        if nutr is not None:
            print(product.capitalize())
            for ind, val in zip(nutr.keys(), nutr.values):
                if round(val) != 0:
                    print(f"{ind} - {round(val)}% of Daily Value")


class SimilarRecipes():
    def __init__(self, epi_link):
        self.epi = pd.read_csv(epi_link)
    
    @staticmethod
    def getProducts(ingr:pd.Series)->set:
        return set(ingr[ingr == 1].index)

    def findSimilar(self, products:list):
        products = set(products)
        list_of_mathches = []
        for ind, row in self.epi.iterrows():
            if self.getProducts(row[10:]).issubset(products):
                list_of_mathches.append((ind, len(self.getProducts(row[7:]))))
        for i in sorted(list_of_mathches, key=lambda x: x[1], reverse=True)[:3]:
            print(f"- {self.epi.loc[i[0]]['title'].strip()}, rating: {self.epi.loc[i[0]]['rating']}, URL: {self.epi.loc[i[0]]['link']}")


class MenuMaker():
    def __init__(self, epi_link):
        self.epi = pd.read_csv(epi_link)

    def printInfo(self, id):
        print('---------------------')

        print(f'{self.epi.loc[id]["title"]}(rating: {self.epi.loc[id]["rating"]})')

        print('Ingredients:')
        for pr in SimilarRecipes.getProducts(self.epi.loc[id][10:]):
            print(f"- {pr}")
        
        print("Nutrients:")
        for i in ['protein', 'fat', 'sodium']:
            print(f'- {i}: {int(self.epi.loc[id][i])}%')

        print(f'URL: {self.epi.loc[id]["link"]}')
       
    def calculateMask(self, br_id, lu_id, threshold):
        prot = self.epi['protein'] + self.epi.loc[br_id]['protein'] + self.epi.loc[lu_id]['protein']
        fat = self.epi['fat'] + self.epi.loc[br_id]['fat'] + self.epi.loc[lu_id]['fat']
        sod = self.epi['sodium'] + self.epi.loc[br_id]['sodium'] + self.epi.loc[lu_id]['sodium']
        mask = ((self.epi['dinner'] == 1) & (self.epi['link'].notna()) & (self.epi['rating'] >= threshold) 
                                       &(prot <= 100)&(prot > 85)
                                       &(fat <= 100)&(fat > 85)
                                       &(sod <= 100)&(sod > 85))
        return mask

    def makeMenu(self, threshold = 4):
        
        br_id = random.choice(self.epi[(self.epi['breakfast'] == 1) & (self.epi['link'].notna()) & (self.epi['rating'] >= threshold)].index)
        lu_id = random.choice(self.epi[(self.epi['lunch'] == 1) & (self.epi['link'].notna()) & (self.epi['rating'] >= threshold)].index)
        
        mask = self.calculateMask(br_id, lu_id, threshold)
        while not mask.any():
            lu_id = random.choice(self.epi[(self.epi['lunch'] == 1) & (self.epi['link'].notna()) & (self.epi['rating'] >= threshold)].index)
            mask = self.calculateMask(br_id, lu_id, threshold)

        di_id = random.choice(self.epi[mask].index)

        print("BREAKFAST")
        self.printInfo(br_id)
        print("LUNCH")    
        self.printInfo(lu_id)
        print('DINNER')
        self.printInfo(di_id)
        
class IngredientsPredict():

    list_of_ingredients = [
    'almond', 'amaretto', 'anchovy', 'anise', 'apple', 'apricot', 'artichoke', 'arugula', 'asparagus', 'avocado',
    'bacon', 'banana', 'barley', 'basil', 'beef', 'beet', 'bell pepper', 'berry', 'blackberry', 'blue cheese',
    'blueberry', 'bok choy', 'bran', 'bread', 'brie', 'broccoli', 'bulgur', 'burrito', 'butter', 'buttermilk',
    'butternut squash', 'cabbage', 'candy', 'cantaloupe', 'capers', 'carrot', 'cashew', 'cauliflower', 'caviar',
    'celery', 'cheddar', 'cheese', 'cherry', 'chestnut', 'chicken', 'chickpea', 'chile pepper', 'chili', 'chive',
    'chocolate', 'coconut', 'cod', 'coriander', 'corn', 'crab', 'cranberry', 'cream cheese', 'cucumber', 'curry',
    'custard', 'dairy', 'date', 'duck', 'egg', 'eggplant', 'endive', 'fennel', 'feta', 'fig', 'fish', 'garlic',
    'goat cheese', 'gouda', 'grape', 'grapefruit', 'green bean', 'green onion/scallion', 'ham', 'hamburger',
    'hazelnut', 'honey', 'hummus', 'ice cream', 'jalapeño', 'kale', 'kiwi', 'lamb', 'lemon', 'lentil', 'lettuce',
    'lima bean', 'lime', 'lobster', 'macaroni and cheese', 'mango', 'maple syrup', 'mayonnaise', 'meatball',
    'melon', 'mint', 'mushroom', 'mussel', 'mustard', 'nutmeg', 'oatmeal', 'olive', 'omelet', 'onion', 'orange',
    'oregano', 'oyster', 'pancake', 'papaya', 'paprika', 'parmesan', 'parsley', 'parsnip', 'pasta', 'peanut',
    'pear', 'pecan', 'pepper', 'persimmon', 'pineapple', 'pistachio', 'pizza', 'plum', 'pomegranate', 'pork',
    'potato', 'poultry', 'prosciutto', 'prune', 'pumpkin', 'quail', 'quinoa', 'radish', 'raisin', 'raspberry',
    'rice', 'ricotta', 'rosemary', 'salmon', 'salsa', 'sausage', 'scallop', 'seafood', 'sesame', 'shallot',
    'shrimp', 'spinach', 'squash', 'steak', 'strawberry', 'sugar snap pea', 'sweet potato/yam', 'swiss cheese',
    'tangerine', 'tapioca', 'tarragon', 'tea', 'thyme', 'tilapia', 'tofu', 'tomato', 'trout', 'tuna', 'turnip',
    'vanilla', 'veal', 'vegetable', 'walnut', 'wasabi', 'watermelon', 'wild rice', 'yellow squash', 'yogurt',
    'zucchini'
]
    
    def __init__(self, input_ingredients):
        self.model = joblib.load('best_recipes_model')
        self.input_ingredients = input_ingredients
        
    def create_X(self):
        dict_of_ingredients = {}

        for ingredient in IngredientsPredict.list_of_ingredients:
            if ingredient in self.input_ingredients:
                dict_of_ingredients[ingredient] = [1.0]
            else:
                dict_of_ingredients[ingredient] = [0.0]
        
        X = pd.DataFrame(dict_of_ingredients, columns = IngredientsPredict.list_of_ingredients)
        return X
    
    def predict_for_list(self):
        flag = 0
        
        for elem in self.input_ingredients:
            if elem not in IngredientsPredict.list_of_ingredients:
                flag = 1
                print('flag = 1')

        if flag == 0:
            print(f'It is a {self.model.predict(self.create_X())[0]} idea to have a dish with that list of ingredients')

class InputCheсker():
    def __init__(self):
        self.ingr_list = ['almond', 'amaretto', 'anchovy', 'anise', 'apple', 'apricot', 'artichoke', 'arugula', 'asparagus', 'avocado',
    'bacon', 'banana', 'barley', 'basil', 'beef', 'beet', 'bell pepper', 'berry', 'blackberry', 'blue cheese',
    'blueberry', 'bok choy', 'bran', 'bread', 'brie', 'broccoli', 'bulgur', 'burrito', 'butter', 'buttermilk',
    'butternut squash', 'cabbage', 'candy', 'cantaloupe', 'capers', 'carrot', 'cashew', 'cauliflower', 'caviar',
    'celery', 'cheddar', 'cheese', 'cherry', 'chestnut', 'chicken', 'chickpea', 'chile pepper', 'chili', 'chive',
    'chocolate', 'coconut', 'cod', 'coriander', 'corn', 'crab', 'cranberry', 'cream cheese', 'cucumber', 'curry',
    'custard', 'dairy', 'date', 'duck', 'egg', 'eggplant', 'endive', 'fennel', 'feta', 'fig', 'fish', 'garlic',
    'goat cheese', 'gouda', 'grape', 'grapefruit', 'green bean', 'green onion/scallion', 'ham', 'hamburger',
    'hazelnut', 'honey', 'hummus', 'ice cream', 'jalapeño', 'kale', 'kiwi', 'lamb', 'lemon', 'lentil', 'lettuce',
    'lima bean', 'lime', 'lobster', 'macaroni and cheese', 'mango', 'maple syrup', 'mayonnaise', 'meatball',
    'melon', 'mint', 'mushroom', 'mussel', 'mustard', 'nutmeg', 'oatmeal', 'olive', 'omelet', 'onion', 'orange',
    'oregano', 'oyster', 'pancake', 'papaya', 'paprika', 'parmesan', 'parsley', 'parsnip', 'pasta', 'peanut',
    'pear', 'pecan', 'pepper', 'persimmon', 'pineapple', 'pistachio', 'pizza', 'plum', 'pomegranate', 'pork',
    'potato', 'poultry', 'prosciutto', 'prune', 'pumpkin', 'quail', 'quinoa', 'radish', 'raisin', 'raspberry',
    'rice', 'ricotta', 'rosemary', 'salmon', 'salsa', 'sausage', 'scallop', 'seafood', 'sesame', 'shallot',
    'shrimp', 'spinach', 'squash', 'steak', 'strawberry', 'sugar snap pea', 'sweet potato/yam', 'swiss cheese',
    'tangerine', 'tapioca', 'tarragon', 'tea', 'thyme', 'tilapia', 'tofu', 'tomato', 'trout', 'tuna', 'turnip',
    'vanilla', 'veal', 'vegetable', 'walnut', 'wasabi', 'watermelon', 'wild rice', 'yellow squash', 'yogurt',
    'zucchini']
    
    @staticmethod
    def preprocess(l):
        return [i.strip(' ,') for i in l]
        
    def check(self, l):
        if  len(l) == 0:
            raise ValueError("No ingredients were entered")
        error_list = []
        for i in l:
            i = i.strip(" ,")
            if not i in self.ingr_list:
                error_list.append(i)
        if len(error_list) != 0:
            raise ValueError(f"following ingredients are missing in our database: {error_list}")
        
