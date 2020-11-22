import os
from flask import (
    Flask, render_template, redirect, flash, url_for, request)
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

"""I copied most of the code above to set up flask from line 1 to 16
& the last "if__name__" code from Tims 2020 Task Manager videos """


@app.route("/")
@app.route("/start")
def start():
    return render_template("start.html")


@app.route("/recipes/<id_for_recipe>")
def recipes(id_for_recipe):
    recipe = mongo.db.recipes.find_one({"_id":  ObjectId(id_for_recipe)})
    return render_template("recipe._detail.html", recipe=recipe)


@app.route("/breakfast")
def breakfast():
    categories = list(mongo.db.recipes.find({"category": "BREAKFAST"}))
    category_name = "BREAKFAST"
    return render_template(
        "category.html", categories=categories, category_name=category_name)


@app.route("/meals")
def meals():
    categories = list(mongo.db.recipes.find({"category": "MEALS"}))
    category_name = "MEALS"
    return render_template(
        "category.html", categories=categories, category_name=category_name)


@app.route("/desserts")
def desserts():
    categories = list(mongo.db.recipes.find({"category": "DESSERTS"}))
    category_name = "DESSERTS"
    return render_template(
        "category.html", categories=categories, category_name=category_name)


@app.route("/smoothies")
def smoothies():
    categories = list(mongo.db.recipes.find({"category": "SMOOTHIES"}))
    category_name = "SMOOTHIES"
    return render_template(
        "category.html", categories=categories, category_name=category_name)


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
        flash("Your Recipe was Successfully Added!")

    return render_template("add_recipe.html")


# I used Tims Task Manager videos as reference for setting up
# the code to update a recipe and customized it for my own needs
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
        flash("Your Recipe was Successfully Updated!")

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("edit_recipe.html", recipe=recipe)


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    flash("Recipe was Successfully Deleted!")
    return render_template("add_recipe.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)