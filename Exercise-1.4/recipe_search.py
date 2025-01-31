import pickle 

def display_recipe(recipe):
    print("Recipe: ", recipe["name"])
    print("Cooking time: ", recipe["cooking_time"])
    print("Ingredients: ")
    for element in recipe["ingredients"]:
        print("-", element)
    print("Difficulty", recipe["difficulty"])

def search_ingredients(data):
    print("Avaiable ingredients: ")
    for index, ingredient in enumerate(data["all_ingredients"]):
        print(f"{index}: {ingredient}")
    try:
        number = int(input("Which ingredient would you like to search for? "))
        ingredient_searched = data["all_ingredients"][number]
    except ValueError:
        print("Invalid selection, try another number ")
    except:
        print("Your number doesn't match any ingredients, try again.")
    else:
        for element in data["recipes_list"]:
            if ingredient_searched in element["ingredients"]:
                print(element)


filename = input("Enter the filename you want to save to ")

try:
    file = open(filename, "rb")
    data = pickle.load(file)
    print("File loaded successfully")
except FileNotFoundError:
    print("File not found, try again")
except:
    print("There was an error")
else:
    file.close()
    search_ingredients(data)
