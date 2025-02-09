# import packages
# importing pymysql because pip install mysqlclient wouldnt work
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker
# replacement for mysqlclient
pymysql.install_as_MySQLdb()

engine = create_engine("mysql+mysqlconnector://cf-python:password@localhost/my_database")

# Store declarative base
Base = declarative_base()

# Create session object to make changes to database
Session = sessionmaker(bind=engine)
session = Session()

# recipe model
class Recipe(Base):
    __tablename__ = "recipe_app"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + "-" + self.name + ">"
    
    # prints full recipe data
    def __str__(self):
        return (
            f"{'-'*10}\n"
            f"Recipe: {self.name}\n"
            f"Cooking Time: {self.cooking_time} minutes\n"
            f"Ingredients: {self.ingredients}\n"
            f"Difficulty: {self.difficulty}\n"
            f"{'-'*10}\n"
        )
    
# function to calculate the difficulty of the recipe
    def calculate_difficulty(self):
        num_ingredients = len(self.return_ingredients_as_list())
        if self.cooking_time < 10 and num_ingredients <= 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 20 and num_ingredients <= 6:
            self.difficulty = "Medium"
        elif self.cooking_time < 30 and num_ingredients <= 8:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        return [ingredient.strip() for ingredient in self.ingredients.split(", ")]

Base.metadata.create_all(engine)

# --- main operation functions --- 

def create_recipe():
    name = input("Enter recipe name (max 50 characters): ")
    while len(name) > 50:
        name = input("Name too long. Enter again (max 50 characters): ")

    num_ingredients = int(input("How many ingredients? "))
    ingredients = []
    for _ in range(num_ingredients):
        ingredient = input("Enter an ingredient: ")
        ingredients.append(ingredient)
    ingredients_str = ", ".join(ingredients)

    cooking_time = input("Enter cooking time (in minutes): ")
    while not cooking_time.isnumeric():
        cooking_time = input("Invalid input. Enter cooking time (in minutes): ")
    cooking_time = int(cooking_time)

    recipe_entry = Recipe(name=name, ingredients=ingredients_str, cooking_time=cooking_time, difficulty="")
    recipe_entry.calculate_difficulty()
    session.add(recipe_entry)
    session.commit()
    print("Recipe created successfully!")

# function to view all recipes
def view_all_recipes():
    recipes = session.query(Recipe).all()
    if not recipes:
        print("No recipes found.")
        return
    for recipe in recipes:
        print(recipe)

# function to search for recipes by an ingredient 
def search_by_ingredients():
    if session.query(Recipe).count() == 0:
        print("No recipes available.")
        return

    results = session.query(Recipe.ingredients).all()
    all_ingredients = []
    for result in results:
        for ingredient in result[0].split(", "):
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)

    print("Available ingredients:")
    for i, ingredient in enumerate(all_ingredients, 1):
        print(f"{i}. {ingredient}")

    selected_numbers = input("Enter ingredient numbers (separated by spaces): ").split()
    search_ingredients = [all_ingredients[int(num) - 1] for num in selected_numbers if num.isnumeric() and 1 <= int(num) <= len(all_ingredients)]

    conditions = [Recipe.ingredients.like(f"%{ingredient}%") for ingredient in search_ingredients]
    recipes = session.query(Recipe).filter(*conditions).all()

    if not recipes:
        print("No recipes found.")
        return

    for recipe in recipes:
        print(recipe)

# function to edit a recipe 
def edit_recipe():
    recipes = session.query(Recipe.id, Recipe.name).all()
    if not recipes:
        print("No recipes available.")
        return

    print("Available recipes:")
    for recipe in recipes:
        print(f"{recipe.id}: {recipe.name}")

    recipe_id = input("Enter the recipe ID to edit: ")
    recipe_to_edit = session.query(Recipe).filter_by(id=recipe_id).first()
    if not recipe_to_edit:
        print("Invalid recipe ID.")
        return

    print("1. Name")
    print("2. Ingredients")
    print("3. Cooking Time")
    choice = input("Enter the number of the field to edit: ")

    if choice == "1":
        new_name = input("Enter new name: ")
        recipe_to_edit.name = new_name
    elif choice == "2":
        num_ingredients = int(input("How many ingredients? "))
        ingredients = []
        for _ in range(num_ingredients):
            ingredient = input("Enter an ingredient: ")
            ingredients.append(ingredient)
        recipe_to_edit.ingredients = ", ".join(ingredients)
    elif choice == "3":
        new_time = input("Enter new cooking time: ")
        while not new_time.isnumeric():
            new_time = input("Invalid input. Enter new cooking time: ")
        recipe_to_edit.cooking_time = int(new_time)
    else:
        print("Invalid choice.")
        return

    recipe_to_edit.calculate_difficulty()
    session.commit()
    print("Recipe updated successfully!")

# function to delete a recipe
def delete_recipe():
    recipes = session.query(Recipe.id, Recipe.name).all()
    if not recipes:
        print("No recipes available.")
        return

    print("Available recipes:")
    for recipe in recipes:
        print(f"{recipe.id}: {recipe.name}")

    recipe_id = input("Enter the recipe ID to delete: ")
    recipe_to_delete = session.query(Recipe).filter_by(id=recipe_id).first()
    if not recipe_to_delete:
        print("Invalid recipe ID.")
        return

    confirm = input("Are you sure you want to delete this recipe? (yes/no): ").lower()
    if confirm == "yes":
        session.delete(recipe_to_delete)
        session.commit()
        print("Recipe deleted successfully!")

# main menu function which allows a user to interact with the a
def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for recipes by ingredients")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("Type 'quit' to exit.")

        choice = input("Enter your choice: ").lower()

        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_by_ingredients()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice == "quit":
            session.close()
            engine.dispose()
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
