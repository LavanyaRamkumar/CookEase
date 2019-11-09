from flask import Flask, request, jsonify
>>>>>>> ce5a76df28188548069e7239e8cd6a38c9a536b1
from flask_restful import Resource, Api
from flask_cors import cross_origin, CORS
import pickle
import json

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r'/*':{"origins": 'http://localhost:4000'}})

def match(recipe, pantry):
	total = len(recipe["ingredients"])
	available = 0
	for ingredient in recipe["ingredients"]:
		if ingredient in pantry:
			available+=1
	return available/total

class Recipes(Resource):
	def get(self):
		args = request.form
		cuisine_query = args["cuisine"]
		type_query = args["type"] 
		pantry = args.getlist("Ingredients")

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
		return [probability, [recipes[key] for _, key in probability]]

class RecipesId(Resource):
	def get(self):
		args = request.form 
		id_list = args.getlist("id")

		answer = []

		for num in id_list:
			answer.append(recipes[num])
		return answer

api.add_resource(Recipes, '/cookease/recipes/')
api.add_resource(RecipesId, '/cookease/recipes/id/')

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
	with open("../data/ingredients.pkl", "rb") as file:
		ingredients = list(pickle.load(file))
	with open("../data/id_recipes.pkl", "rb") as file:
		recipes = pickle.load(file)
	app.run(debug=True)
