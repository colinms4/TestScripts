import pickle 

def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and int(ingredients) < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and int(ingredients) >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and int(ingredients) < 4:
        difficulty = "Intermediate"
    else:
        difficulty = "Hard"
    return difficulty


# Function to take recipe details from the user
def take_recipe():
    recipe_name = input("Enter the recipe name: ")
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    ingredients = input("Enter the ingredients (comma-separated): ").split(",")
    ingredients = [ingredient.strip() for ingredient in ingredients]
    difficulty = calc_difficulty(cooking_time, len(ingredients))
    return {"name": recipe_name, "cooking_time": cooking_time, "ingredients": ingredients, "difficulty": difficulty}

# Main code
filename = input("Enter the filename to load/save recipes: ")

try:
    file = open(filename, "rb")
    data = pickle.load(file)
    print("File Loaded Successfully")
except FileNotFoundError:
    print("File not found")
    data = {"recipes_list": [], "all_ingredients": []}
except:
    print("Something went wrong, try again.")
    data = {"recipes_list": [], "all_ingredients": []}
else: 
    file.close()
finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]


n = int(input("How many recipes would you like to enter? "))

for i in range(0,n):
    recipe = take_recipe()
    for element in recipe["ingredients"]:
        if element not in all_ingredients:
            all_ingredients.append(element)
    recipes_list.append(recipe)
    print("Recipe successfully added")

#stores a dictionary with updated data
data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}

#Save the recipe to a file
updated_file = open(filename,  "wb")
pickle.dump(data, updated_file)
#close file
updated_file.close()
print("Recipe has been saved")