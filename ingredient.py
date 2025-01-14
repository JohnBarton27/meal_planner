#!/usr/bin/env python3

from database import Database

class Ingredent:

	db_obj = Database()
	
	def __init__(self, name, id = 0, category = "", quantity = 1, unit = ""):
	
		self.name = name
		self.id = id
		self.category = category
		self.quantity = quantity
		self.unit = unit
		
	def __repr__(self):
		return self.name

	# This is used to compare ingredients to others
	def __eq__(self, other):
		return self.name.lower() == other
		
	def insert_ingredient(self):
		"""
		This will insert an ingredient into our database

		Args:
			conn (Connection): This is the connection to our db
		"""

		Ingredent.db_obj.execute("INSERT INTO ingredients(name, category) VALUES (?, ?)", (self.name, self.category))
			
	@staticmethod
	def list_ingredients():
		"""
		This will return all the ingredients in our database
		
		Args:
			conn (Connection): This is the connection to our db
		Returns:
			sqlite3.Row Obj: Ingredient rows 
		"""
		
		ingredients = Ingredent.db_obj.execute('SELECT * FROM ingredients').fetchall()
		
		# Lets turn these into objects
		ingredient_objs = []
		
		for ing in ingredients:
			ingredient_obj = Ingredent(ing['name'], ing['id'], ing['category'])
			
			ingredient_objs.append(ingredient_obj)
			
		return ingredient_objs

	@staticmethod
	def get_ingredient(id, quantity, unit):
		"""
		Retruns an ingredient obj
		"""
		
		# Get the data for this ingredient
		ingredient_row = Ingredent.db_obj.execute(f"SELECT name, category FROM ingredients where id = '{id}'").fetchone()

		# Instantiate an Ingredent object with eveyrthing it needs
		ing_obj = Ingredent(ingredient_row['name'], id, ingredient_row['category'], quantity, unit)
		return ing_obj

	@staticmethod
	def ingredient_combiner(recipes):
		"""
		Given a list of Recipe Objects, return a list of all the required ingredient objects

		Args:
			Recipe[]:  List of recipe objects

		Returns:
			Ingredient{}: Dict with ingredient names and their quantities
		
		"""

		# Lets use a dict where the keys are the ingredient names and values is quantity
		ingredient_dict = {}

		# Need to get a total count of each ingredient for each recipe
		for recipe in recipes:
			print(f"{recipe.name = }")
			for ingredient in recipe.ingredients:

				# We need to insert or update the count of this ingredient
				if ingredient.name in ingredient_dict:
					ingredient_dict[ingredient.name] += ingredient.quantity
				else:
					ingredient_dict[ingredient.name] = ingredient.quantity

		return ingredient_dict
