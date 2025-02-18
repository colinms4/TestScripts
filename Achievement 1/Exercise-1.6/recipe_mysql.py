import mysql.connector

# connection to database
conn = mysql.connector.connect(
    host="localhost",
    user="cf-python",
    passwd="password"
)

cursor = conn.cursor()

# create db
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")

# create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Recipes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50),
        ingredients VARCHAR(255),
        cooking_time INT,
        difficulty VARCHAR(20)
    )
""")

# main menu screen function
def main_menu(conn, cursor):
    while True:
        print("\nRecipe App Menu:")
        print("1. Add a new recipe")
        print("2. Search for a recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            create_recipe(conn, cursor)
        elif choice == "2":
            search_recipe(conn, cursor)
        elif choice == "3":
            update_recipe(conn, cursor)
        elif choice == "4":
            delete_recipe(conn, cursor)
        elif choice == "5":
            conn.commit()
            conn.close()
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

# function to calculate the difficulty of the recipe
def calculate_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        return "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        return "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        return "Intermediate"
    else:
        return "Hard"

# function to create a recipe and add it to the db
def create_recipe(conn, cursor):
    name = input("Enter recipe name: ")
    cooking_time = int(input("Enter cooking time in minutes: "))
    ingredients = input("Enter ingredients (comma-separated): ").split(", ")
    
    difficulty = calculate_difficulty(cooking_time, ingredients)
    ingredients_str = ", ".join(ingredients)
    
    query = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, ingredients_str, cooking_time, difficulty))
    conn.commit()
    print("Recipe added successfully!")

# function to search for a recipe with a list of ingredients
def search_recipe(conn, cursor):
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()

    all_ingredients = set()
    for result in results:
        ingredients = result[0].split(", ")
        all_ingredients.update(ingredients)
    
    print("\nAviable Ingredients: ")
    for i, ingredient in enumerate(sorted(all_ingredients), 1):
        print(f"{i}. {ingredient}")
    
    choice = int(input("Choose an ingredient by number: "))
    search_ingredient = list(sorted(all_ingredients))[choice - 1]

    query = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
    cursor.execute(query,(f"%{search_ingredient}%",))
    recipes = cursor.fetchall()

    if recipes:
        print("\nRecipes Found: ")
        for recipe in recipes:
            print(recipe)
    else:
        print("No recipe found with that ingredient")

# function to update an existing recipe
def update_recipe(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    recipes = cursor.fetchall()
    
    print("\nAvailable recipes:")
    for recipe in recipes:
        print(recipe)
    
    recipe_id = int(input("Enter the ID of the recipe to update: "))
    column = input("Which field would you like to update (name, cooking_time, ingredients)? ").lower()
    
    if column == "cooking_time":
        new_value = int(input("Enter the new cooking time: "))
        cursor.execute(f"UPDATE Recipes SET {column} = %s WHERE id = %s", (new_value, recipe_id))
        
        cursor.execute("SELECT ingredients FROM Recipes WHERE id = %s", (recipe_id,))
        ingredients_str = cursor.fetchone()[0]
        ingredients = ingredients_str.split(", ")
        difficulty = calculate_difficulty(new_value, ingredients)
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (difficulty, recipe_id))
    
    elif column == "ingredients":
        new_value = input("Enter the new ingredients (comma-separated): ")
        ingredients = new_value.split(", ")
        cursor.execute(f"UPDATE Recipes SET {column} = %s WHERE id = %s", (new_value, recipe_id))
        
        cursor.execute("SELECT cooking_time FROM Recipes WHERE id = %s", (recipe_id,))
        cooking_time = cursor.fetchone()[0]
        difficulty = calculate_difficulty(cooking_time, ingredients)
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s", (difficulty, recipe_id))
    
    else:
        new_value = input("Enter the new value: ")
        cursor.execute(f"UPDATE Recipes SET {column} = %s WHERE id = %s", (new_value, recipe_id))
    
    conn.commit()
    print("Recipe updated successfully!")

# function to delete a recipe 
def delete_recipe(conn, cursor):
    cursor.execute("SELECT * FROM Recipes")
    recipes = cursor.fetchall()
    
    print("\nAvailable recipes:")
    for recipe in recipes:
        print(recipe)
    
    recipe_id = int(input("Enter the ID of the recipe to delete: "))
    cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id,))
    conn.commit()
    print("Recipe deleted successfully!")

# runs the main menu function to allow users to interact with the script
if __name__ == "__main__":
    main_menu(conn, cursor)
