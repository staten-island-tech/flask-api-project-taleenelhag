from flask import Flask, render_template, request
import requests

app = Flask(__name__)
API_URL = "https://rickandmortyapi.com/api/character"
cached_characters = []

def format_character(c):
    return {
        "id": c.get("id"),
        "name": c.get("name", "Unknown"),
        "status": c.get("status", "Unknown"),
        "species": c.get("species", "Unknown"),
        "gender": c.get("gender", "Unknown"),
        "origin": c.get("origin", {}).get("name", "Unknown"),
        "image": c.get("image", "/static/placeholder.jpg")
    }

@app.route("/")
def index():
    global cached_characters
    search = request.args.get("search", "")
    page = request.args.get("page", "1")

    try:
        response = requests.get(API_URL, params={"page": page, "name": search})
        data = response.json()
        characters = data.get("results", [])

        character_list = [format_character(c) for c in characters]
        cached_characters = character_list

        return render_template("index.html", character_list=character_list, search_text=search)

    except:
        return "Sorry, something went wrong.", 500

@app.route("/character/<int:char_id>")
def character_detail(char_id):
    for character in cached_characters:
        if character["id"] == char_id:
            return render_template("detail.html", character=character)
    return "Character not found", 404

if __name__ == "__main__":
    app.run(debug=True)


