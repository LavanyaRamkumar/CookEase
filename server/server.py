from flask import Flask
from flask_restful import Resource, Api
import pickle

app = Flask(__name__)
api = Api(app)

class Recipes(Resource):
	def get(self):
		return recipes[list(recipes.keys())[0]]

api.add_resource(Recipes, '/cookease/recipes/')

if __name__ == '__main__':
	with open("../data/ingredients.pkl", "rb") as file:
		ingredients = list(pickle.load(file))
	with open("../data/id_recipes.pkl", "rb") as file:
		recipes = pickle.load(file)
	app.run(debug=True)