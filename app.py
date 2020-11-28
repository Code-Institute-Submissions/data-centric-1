""" I have used Tim's Task Manager videos a lot as
a reference throughout my whole project
and for making the code in this 'app.py' file """

import os
from flask import (
    Flask, render_template, flash, redirect, url_for, request)
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/start")
def start():
    return render_template("start.html")


@app.route("/all_recipes")
def all_recipes():
    # For showing all recipes in the All Recipes page
    all_recipes = list(mongo.db.recipes.find())
    return render_template("all_recipes.html", all_recipes=all_recipes)


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    This code was used from Tim's Task Manager videos
    for making the search input work for getting
    search results in All Recipes page
    """
    index_search = request.form.get("index_search")
    all_recipes = list(mongo.db.recipes.find({
        "$text": {"$search": index_search}}))
    return render_template("all_recipes.html", all_recipes=all_recipes)


@app.route("/recipes/<id_for_recipe>")
def recipes(id_for_recipe):
    """
    This is to view the full recipe information for
    a specific recipe when clicking on its belonging
    recipe image or recipe name.
    """
    recipe = mongo.db.recipes.find_one({"_id":  ObjectId(id_for_recipe)})
    return render_template("recipe_detail.html", recipe=recipe)


@app.route("/<category_name>")
def recipes_by_category(category_name):
    """
    My mentor helped me to create and improve the route for
    categories for avoiding the code to be repetitive
    with several routes for each category that I created
    before.
    This is for making the recipes display
    in a category grouped by a common category name when
    clicking on a link in the category menu in the navbar.
    """
    categories = list(mongo.db.recipes.find({
        "category": category_name.upper()}))
    return render_template(
        "category.html", categories=categories,
        category_name=category_name.upper())


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        recipe = {
            "category": request.form.get("category"),
            "image": request.form.get("image"),
            "time": request.form.get("time") + " minutes",
            "portions": request.form.get("portions"),
            "recipe_name": request.form.get("recipe_name"),
            "ingredients": list(filter(None, request.form.getlist(
                "ingredients"))),
            "instructions": list(filter(None, request.form.getlist(
                "instructions"))),
            "added_by": request.form.get("added_by")
        }

        """
        For inserting an added recipe on the page and
        in Mongo DB after the user has submitted the 
        form on the Add Recipe page.
        """
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe was Successfully Added!")
        return redirect(url_for("all_recipes"))
    return render_template("add_recipe.html")


# For Updating a Recipe
@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    if request.method == "POST":
        update_recipe = {
            "category": request.form.get("category"),
            "image": request.form.get("image"),
            "time": request.form.get("time") + " minutes",
            "portions": request.form.get("portions"),
            "recipe_name": request.form.get("recipe_name"),
            "ingredients": list(filter(None, request.form.getlist(
                "ingredients"))),
            "instructions": list(filter(None, request.form.getlist(
                "instructions"))),
            "added_by": request.form.get("added_by")
        }

        """
        For inserting the Updated recipe in the page and Mongo
        DB after the user has updated the recipe and submitted
        the form on the Edit Recipe page.
        The recipe is then extracted for showing the recipe
        information in the form inputs when the user wants to
        update and change the recipe information.
        """
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, update_recipe)
        flash("Recipe was Successfully Updated!")
        return redirect(url_for("all_recipes"))
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("edit_recipe.html", recipe=recipe)


# For Deleting a Reicpe
@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    """
    This code is for deleting the recipe
    when clicking the Delete Recipe button on
    the Edit Recipe page and then redirecting
    to the All Recipes page.
    """
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe was Successfully Deleted!")
    return redirect(url_for("all_recipes"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)