from flask import Flask, render_template, request
import datetime
import requests
import json
import os

app = Flask(__name__)

ct = datetime.datetime.now()
current_year = ct.year

CACHE_FILE = "static/pokemon_cache.json"
API_URL = "https://pokeapi.co/api/v2/pokemon/"

def load_or_create_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    else:
        pokemon_list = []
        for id in range(1, 152):
            response = requests.get(f"{API_URL}{id}")
            data = response.json()
            pokemon = {
                "id": id,
                "name": data["name"],
                "types": [t["type"]["name"] for t in data["types"]],
                "image": data["sprites"]["front_default"]
            }
            pokemon_list.append(pokemon)
        with open(CACHE_FILE, "w") as f:
            json.dump(pokemon_list, f, indent=2)
        return pokemon_list

pokemon_list = load_or_create_cache()

@app.route('/')
def main_page():
    query = request.args.get('search')
    if query:
        query = query.lower()
        try:
            response = requests.get(f"{API_URL}{query}")
            response.raise_for_status()
            data = response.json()
            pokemon = {
                "id": data["id"],
                "name": data["name"],
                "types": [t["type"]["name"] for t in data["types"]],
                "image": data["sprites"]["front_default"]
            }
            return render_template("index.html", all_pokemon=[pokemon], current_year=current_year)
        except:
            return render_template("index.html", all_pokemon=[], current_year=current_year, error="Pokémon not found!")

    return render_template("index.html", all_pokemon=pokemon_list, current_year=current_year)

if __name__ == "__main__":
    app.run(debug=True)

