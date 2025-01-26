#empty lists for recipes and ingredients 
recipes_list = []
ingredients_list = []

#allows a user to input recipe names, ingredients, and cooking time
def take_recipe():
    name = str(input("Enter the name of the recipe: "))
    cooking_time = int(input("Enter the cooking time: "))
    ingredients = list(input("Enter the ingredients: ").split(", "))
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients
    }
    return recipe

n = int(input("How many recipes would you like to enter? "))

#iterates over the data input 
for i in range(n):
    recipe = take_recipe()

    for ingredient in recipe["ingredients"]:
        if not ingredient in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)


for recipe in recipes_list:
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4: 
        recipe["difficulty"] = "medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "intermediate"
    elif recipe["cooking_time"] >= 10  and len(recipe["ingredients"]) >=4:
        recipe["difficulty"] = "hard"
    
    print("Recipe: ", recipe["name"])
    print("Cooking Time: ", recipe["cooking_time"])
    print("Ingredients: ", recipe["ingredients"])
    print("Difficulty: ", recipe["difficulty"])

def all_ingredients():
    ingredients_list.sort()
    print("Ingredients available for all recipes")
    print("--------------------------------------")
    for ingredient in ingredients_list:
        print(ingredient)

all_ingredients()


