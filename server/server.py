from flask import *
from flask_restful import Resource, Api
from flask_cors import cross_origin, CORS
import pickle
import json
import atexit
import os
from werkzeug.utils import secure_filename
import subprocess



app = Flask(__name__, static_folder='static')
api = Api(app)
#cors = CORS(app, resources={r'/*':{"origins": 'http://localhost:4000'}})
cors = CORS(app)

@app.route("/")
def index():
	return (render_template("index.html"))

@app.route("/menu.html")
def menu():
	return (render_template("menu.html"))

@app.route("/add_recipe", methods=['GET', 'POST'])
def add_recipe_html():
	if request.method=="GET":
		a=set()
		b=set()
		for i in recipes.values():
			a.add(i["type"])
			b.add(i["cuisine"])
		print(a,b)
		# return jsonify(recipes)
		return (render_template("add_recipe.html"))
	else:
		print(request.form)
		file = request.files['file']
		file.save("./static/data/food_images/temp.jpg")
		id=20482
		return (render_template("view_recipe.html",id=str(id)))


@app.route("/view_recipe/<id>")
def view_recipe_by_id(id):
	#id=20482
	return (render_template("view_recipe.html",id=str(id)))

@app.route("/pf")
def view_recipe_html():
	return (render_template("pf_msd.html"))

@app.route("/c/<cuisine>")
def c(cuisine):
	return (render_template("particular_cuisine.html", data = cuisine))

@app.route("/groceries")
def groceries():
	return (render_template("trial_grocery.html"))

def match(recipe, pantry):
	total = len(recipe["ingredients"])
	available = 0
	for ingredient in recipe["ingredients"]:
		if ingredient in pantry:
			available+=1
	return available/total



class Recipes(Resource):
	def post(self):
		args = request.form
		cuisine_query = args["cuisine"]
		type_query = args["type"] 
		pantry = args.getlist("Ingredients")
		pantry = [a.lower() for a in pantry]
		count = int(args["count"])
		if pantry==None:
			pantry = []

		answers = list(recipes.keys())

		if cuisine_query!="":
			temp_answers = []
			for key in answers:
				if recipes[key]["cuisine"]==cuisine_query:
					temp_answers.append(key)
			answers = temp_answers

		if type_query!="":
			temp_answers = []
			for key in answers:
				if recipes[key]["type"]==type_query:
					temp_answers.append(key)
			answers = temp_answers

		probability = []
		for key in answers:			
			probability.append((match(recipes[key], pantry), key))
		
		probability.sort(reverse=True)

		for _,key in probability:
			recipes[key]["key"] = key
		prob, lis = [probability, [recipes[key] for _, key in probability]]
		startIndex = count*6
		endIndex = count*6+6
		return jsonify({"prob":prob[startIndex:endIndex],"recipes":lis[startIndex:endIndex]})	


class RecipesId_initial(Resource):
	def get(self,id):
		try:
			return jsonify(recipes[int(id)])
		except:
			return jsonify({})

class RecipesId_recipe(Resource):
	def get(self,id):
		try:
			d={}
			with open('static/data/items/'+str(id)+'.json') as f:
				d = json.load(f)
				# print(d)
			return jsonify(d)
		except:
			return jsonify({})

class getIngredients(Resource):
	def get(self, match_str):
		ing_types = ingredients.keys()
		print(ing_types)
		match_str = match_str.lower()
		answers = []
		for ing in ing_types:
			temp = [i for i in ingredients[ing] if match_str==i[:len(match_str)]]
			answers+=temp

		answers = sorted(answers, key=lambda x:x.replace(' ', ''))
		return jsonify(sorted(answers, key=lambda x: ''.join(x.split()), reverse=True))

class getCategory(Resource):
	def get(self, match_str):
		ing_types = ingredients.keys()

		match_str = match_str.lower()
		answer = "Other"
		for ing in ing_types:
			if match_str in ingredients[ing]:
				answer = ing
				break
		print(answer)
		if answer=='Condiment':
			answer = "Herbs and Spices"
		return jsonify(answer)

@app.route("/cookease/bill/", methods=['GET', 'POST'])
def convertBill():
	if request.method=="POST":
		bill = request.files['bill']
		bill.save("./static/temp/temp.jpg")
		print("done")
		return render_template('bill.html')

	else:

		output = subprocess.check_output("python3 items.py ./static/temp/temp.jpg", shell=True)
		return output.decode("utf-8")



api.add_resource(Recipes, '/cookease/recipes/')
api.add_resource(RecipesId_initial, '/cookease/recipes/title/id/<id>')
api.add_resource(RecipesId_recipe, '/cookease/recipes/recipe/id/<id>')
api.add_resource(getIngredients, '/cookease/ingredient/<match_str>')
api.add_resource(getCategory, '/cookease/category/<match_str>')
# api.add_resource(convertBill, '/cookease/bill/')

class Test(Resource):
	def get(self):
		return "hello world"
api.add_resource(Test, '/')

class GetCuisines(Resource):
	def get(self):
		# images are located at static/assets/images/cuisines/file_name.jpg
		return jsonify({
			"Mexican":"Mexican.jpg",
			"Italian":"Italian.jpg",
			"Indian":"Indian.jpg",
			"Thai":"Thai.jpg"
		}
		)
api.add_resource(GetCuisines, '/get_cuisines')

def goodbye():
	print("saving..")
	with open("static/data/categorical_ingredients", "wb") as file:
		pickle.dump(ingredients,file)
	with open("static/data/id_recipes.pkl", "wb") as file:
		pickle.dump(recipes,file)
	print("saved")


if __name__ == '__main__':
	with open("static/data/categorical_ingredients", "rb") as file:
		ingredients = pickle.load(file)
	with open("static/data/id_recipes.pkl", "rb") as file:
		recipes = pickle.load(file)
	atexit.register(goodbye)
	app.run(debug=True)
