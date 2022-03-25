#!/usr/bin/env python3

import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

from ingredient import Ingredent
from recipe import Recipe

from database import Database

db_obj = Database()

# This will return a database connection to our SQLite db
# This will return rows from the db that are just dicts
def get_db_connection():
	conn = sqlite3.connect('database.db')
	conn.row_factory = sqlite3.Row
	return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkeyohwowcrazy'

"""
================================================================================
|																			   |
|				 Below are the app routes which give route us to  pages		   |
|																			   |
================================================================================
"""


# This is just for the base home page route
@app.route('/')
def index():
	
	# Next lets get all the recipes
	recipes = Recipe.get_selected_recipes()

	# Need to pass in a full list of ingredients we need for all these recipes
	ingredient_dict = Ingredent.ingredient_combiner(recipes)
	
	# We render this page by passing in the posts we just returned from the db
	return render_template('index.html', recipes=recipes)


#~~~~~~~~This is our route to see a recipe~~~~~~~~
@app.route('/<int:recipe_id>')
def recipe(recipe_id):

	# Get this recipe object
	recipe_obj = Recipe.get_recipe(id=recipe_id)

	recipe_obj.selected

	return render_template('recipe.html', recipe=recipe_obj)


#~~~~~~~~This is our route to create a new recipe~~~~~~~~
@app.route('/create', methods=('GET', 'POST')) 
def create():
	
	# Get the ingredients for auto complete
	ingredients = Ingredent.list_ingredients()
		
	# Checks if a post was sent
	if request.method == 'POST':
		# If so grab the input data from the page submitted
		name = request.form['name']
		notes = request.form['notes']
		cuisine = request.form['cuisine']

		# Get ingredients from form
		needed_ingredients = request.values.getlist('ingredients')
		
		if not name:
			flash('Name is required!')
		else:
			recipe_id = Recipe.instert_recipe(name, needed_ingredients, notes, cuisine)

			return recipe(recipe_id)
		
	return render_template('create.html', ingredients=ingredients)


#~~~~~~~~This is our route to add a new ingredient~~~~~~~~
@app.route('/create_ingredient', methods=('GET', 'POST'))
def add_ingredient():
	
	# Checks if a post was sent
	if request.method == 'POST':
		# If so grab the input data from the page submitted
		name = request.form['name']
		category = request.form['category']
	
		if not name:
			flash('Name is required!')
			
		else:
			# Lets write this to the database!
			ing_obj = Ingredent(name, category=category)
			ing_obj.insert_ingredient()
			return redirect(url_for('index'))
	
	return render_template('add_ingredient.html')
		
	


#~~~~~~~~This will edit a recipe~~~~~~~~  NEED TO DO SOMETHING WITH THE STILL ~~~~~~~~ 
@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
	
	# This will get the ID that was selected
	post = get_post(id)
	
	if request.method == 'POST':
		title = request.form['title']
		content = request.form['content']
		
		if not title:
			flash('Title is required!')
		else:
			conn = get_db_connection()
			conn.execute('UPDATE posts SET title = ?, content = ?'' WHERE id = ?', (title, content, id))
			conn.commit()
			conn.close()
			return redirect(url_for('index'))
		
	return render_template('edit.html', post=post)


@app.route('/plan_meals', methods=('GET', 'POST'))
def plan_meals():
	
	# Next lets get all the recipes
	recipes = Recipe.list_recipes()

	#~~~~~~~~~~~~~~DO I NEED THIS IF STATEMENMT HERE?!~~~~~~~~~~~~~~
	if request.method == 'POST':

		# First lets wipe the data in the meal plan, since we already have current values selected
		Recipe.wipe_meal_plan()

		# Get selected recipes from
		selected_recipes = request.values.getlist('recipes')

		# Need a way to convert a name into an id
		for recipe in selected_recipes:

			# First lets get its id
			recipe_id = Recipe.get_id_from_name(recipe)
			Recipe.add_to_meal_plan(recipe_id)


	return render_template('meal_plan.html', recipes=recipes)