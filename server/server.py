from flask import *
from flask_restful import Resource, Api
from flask_cors import cross_origin, CORS
import pickle
import json



app = Flask(__name__, static_folder='static')
api = Api(app)
#cors = CORS(app, resources={r'/*':{"origins": 'http://localhost:4000'}})
cors = CORS(app)

@app.route("/")
def index():
	return (render_template("index.html"))

# @app.route("/menu.html")
# def menu():
# 	return (render_template("menu.html"))

@app.route("/pf")
def pf():
	return (render_template("pf_msd.html"))

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
		#print(probability)
		for _,key in probability:
			recipes[key]["key"] = key
		prob, lis = [probability, [recipes[key] for _, key in probability]]
		startIndex = count*6
		endIndex = count*6+6
		return jsonify({"prob":prob[startIndex:endIndex],"recipes":lis[startIndex:endIndex]})	

class RecipesId(Resource):
	def get(self):
		args = request.form 
		id_list = args.getlist("id")

		answer = []
		print(recipes)
		for num in id_list:
			answer.append(recipes[int(num)])
		return answer

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


api.add_resource(Recipes, '/cookease/recipes/')
api.add_resource(RecipesId, '/cookease/recipes/id/')
api.add_resource(getIngredients, '/cookease/ingredient/<match_str>')
api.add_resource(getCategory, '/cookease/category/<match_str>')

class Test(Resource):
	def get(self):
		return "hello world"
api.add_resource(Test, '/')

class GetCuisines(Resource):
	def get(self):
		# images are located at ui/assets/images/cuisines/file_name.jpg
		return jsonify({
			"Mexican":"Mexican.jpg",
			"Italian":"Italian.jpg",
			"Indian":"Indian.jpg",
			"Thai":"Thai.jpg"
		}
		)
api.add_resource(GetCuisines, '/get_cuisines')

if __name__ == '__main__':
	with open("static/data/categorical_ingredients", "rb") as file:
		ingredients = pickle.load(file)
	with open("static/data/id_recipes.pkl", "rb") as file:
		recipes = pickle.load(file)
	app.run(debug=True)
