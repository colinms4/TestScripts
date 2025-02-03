class Recipe:
    # variable to store unique ingredients from all recipes
    all_ingredients = set()

    # initialization method 
    def __init__(self, name, cooking_time):
        self.name = name
        self.cooking_time = cooking_time
        self.ingredients = []
        self.difficulty = None

    def get_name(self):
        return self.name
    
    def get_cooking_time(self):
        return self.cooking_time
    
    def set_name(self, name):
        self.name = name
    
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time

    def get_ingredients(self):
        return self.ingredients
    
    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            Recipe.all_ingredients.add(ingredient)
    
    def add_ingredients(self, *ingredients):
        for ingredient in ingredients:
            self.ingredients.append(ingredient)
        self.update_all_ingredients()
    
    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"
    
    def get_difficulty(self):
        if not self.difficulty:
            self.calculate_difficulty()
        return self.difficulty

    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients
    
    def __str__(self):
        self.calculate_difficulty()
        return f"Recipe Name: {self.name}\nIngredients: {', '.join(self.ingredients)}\nCooking Time: {self.cooking_time}\nDifficulty: {self.difficulty}"

def recipe_search(data, search_term):
    for recipe in data:
         if recipe.search_ingredient(search_term):
            print(recipe)

tea = Recipe("Tea", 5)
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
print(tea)

coffee = Recipe("Coffee", 5)
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
print(coffee)

cake = Recipe("Cake", 50)
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
print(cake)

banana_smoothie =  Recipe("Banana Smoothie", 5)
banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
print(banana_smoothie)

recipes_list = [tea, coffee, cake, banana_smoothie]

print("\nRecipes containing water: ")
recipe_search(recipes_list, "Water")

print("\nRecipes containing Sugar: ")
recipe_search(recipes_list, "Sugar")

print("\nRecipes containing Bananas: ")
recipe_search(recipes_list, "Bananas")
