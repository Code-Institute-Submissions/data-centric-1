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


# To display all recipes in All Recipes page
@app.route("/all_recipes")
def all_recipes():
    all_recipes = list(mongo.db.recipes.find())
    return render_template("all_recipes.html", all_recipes=all_recipes)


# To get search results in All Recipes page
@app.route("/search", methods=["GET", "POST"])
def search():
    index_search = request.form.get("index_search")
    all_recipes = list(mongo.db.recipes.find({
        "$text": {"$search": index_search}}))
    return render_template("all_recipes.html", all_recipes=all_recipes)


# To view the full recipe information
@app.route("/recipes/<id_for_recipe>")
def recipes(id_for_recipe):
    recipe = mongo.db.recipes.find_one({"_id":  ObjectId(id_for_recipe)})
    return render_template("recipe_detail.html", recipe=recipe)


# In the menu, BREAKFAST
@app.route("/breakfast")
def breakfast():
    categories = list(mongo.db.recipes.find({"category": "BREAKFAST"}))
    category_name = "BREAKFAST"
    return render_template(
        "category.html", categories=categories, category_name=category_name)


# In the menu, MEALS
@app.route("/meals")
def meals():
    categories = list(mongo.db.recipes.find({"category": "MEALS"}))
    category_name = "MEALS"
    return render_template(
        "category.html", categories=categories, category_name=category_name)


# In the menu, DESSERTS
@app.route("/desserts")
def desserts():
    categories = list(mongo.db.recipes.find({"category": "DESSERTS"}))
    category_name = "DESSERTS"
    return render_template(
        "category.html", categories=categories, category_name=category_name)


# In the menu, SMOOTHIES
@app.route("/smoothies")
def smoothies():
    categories = list(mongo.db.recipes.find({"category": "SMOOTHIES"}))
    category_name = "SMOOTHIES"
    return render_template(
        "category.html", categories=categories, category_name=category_name)


# For Adding a new Recipe
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

        mongo.db.recipes.insert_one(recipe)
        flash("Recipe Successfully Added!")
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

        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, update_recipe)
        flash("Recipe Successfully Updated!")
        return redirect(url_for("all_recipes"))

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("edit_recipe.html", recipe=recipe)


# For Deleting a Reicpe
@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe Successfully Deleted!")
    return redirect(url_for("all_recipes"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)