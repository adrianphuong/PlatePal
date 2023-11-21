from flask import Flask, request, render_template, redirect, url_for,session
import requests, pprint
from urllib.parse import unquote

app = Flask(__name__)

spoonacularAPI = "b18e0c13dc9a4376a8ad4f4e45d3a640"

@app.route('/')
def index():
    return render_template(
    'welcome.html')

@app.route('/process_name', methods=['POST'])
def process_name():
    # Get the user's name from the form submission
    name = request.form.get('fname')

    # Redirect to the 'hello' route with the name as a parameter
    return redirect(url_for('hello', name=name))

@app.route('/myfavorites', methods = ['POST'])
def favorites():
    if request.method == 'POST':
        return render_template('favorites.html')

@app.route("/hello/<string:name>/", methods=['GET', 'POST'])
def hello(name):
    if request.method == 'POST':
        # If a form is submitted
        query = request.form.get('search_query', '')
        # Perform a search for recipes with the given query
        recipes = search_recipes(query)
        # Render the main page with the search results and the search query
        return render_template('index.html',name = name, recipes=recipes, search_query=query)
    search_query = request.args.get('search_query', '')
    decoded_search_query = unquote(search_query)
    recipes = search_recipes(decoded_search_query)
    return render_template('index.html', name = name, recipes=recipes, search_query=decoded_search_query)

def search_recipes(query):
    url = f'https://api.spoonacular.com/recipes/complexSearch'
    params = {
        'apiKey': spoonacularAPI,
        'query': query,
        'number': 10,
        'instructionsRequired': True,
        'addRecipeInformation': True,
        'fillIngredients': True,
    }

    # Send a GET request to the Spoonacular API with the query parameters
    response = requests.get(url, params=params)
    # If the API call is successful
    if response.status_code == 200:
        # Parse the API response as JSON data
        data = response.json()
        # Return the list of recipe results
        return data['results']
    # If the API call is not successful
    return []

    


'''
- Use Spoonacular to get Recipe Info
'''


'''def searchByIngredient(api_key, ingredient):
    url = 'https://api.spoonacular.com/recipes/findByIngredients'
    params = {
        "apikey": api_key,
        "ingredients": ingredient
    }
    response = requests.get(url, params = params)

    if response.status_code == 200:
        recipes = response.json()
        print(recipes)
        return recipes
    else:
        return None
    
@app.route('/search', methods = ['POST'])
def search_recipes():
    api_key ="b18e0c13dc9a4376a8ad4f4e45d3a640"
    recipes = searchByIngredient(api_key, ingredient)
    return jsonify({'recipes': recipes})

queryparams = "apiKey=" + spoonacularAPI + \
                "&ingredient" + "egg"
url = 'https://api.spoonacular.com/recipes/findByIngredients'
query = url + "?" + queryparams
resp = requests.get(query)
pprint.pprint(resp.json())'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
