from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

def fetch_fbi_data(params=None):
    base_url = "https://api.fbi.gov/wanted/v1/list"
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() 
        return response.json().get("items", [])
    except Exception as e:
        print(f"API Error: {e}")
        return []

@app.route("/")
def index():
    wanted_list = fetch_fbi_data({"page": 2})
    return render_template("index.html", wanted=wanted_list)

@app.route("/wanted/<uid>")
def wanted_detail(uid):
    items = fetch_fbi_data({"page": 2}) 
    try:
        person = next((p for p in items if p.get("uid") == uid), None)
        if not person:
            raise ValueError("Person not found")
    except Exception as e:
        return render_template("error.html", message=str(e)), 404

    return render_template("wanted.html", person=person)

@app.route("/search")
def search():
    query = request.args.get("query", "").strip().lower()
    all_items = fetch_fbi_data({"page": 2})

    results = [
        item for item in all_items
        if query in item.get("title", "").lower() or query in item.get("details", "").lower()
    ]

    return render_template("index.html", wanted=results)

@app.route("/sort/<key>")
def sort_by(key):
    items = fetch_fbi_data({"page": 2})
    try:
        if key == "title":
            items.sort(key=lambda x: x.get("title", ""))
        elif key == "reward":
            items.sort(key=lambda x: x.get("reward_text", ""))
        elif key == "publication":
            items.sort(key=lambda x: x.get("publication", ""))
    except Exception as e:
        return render_template("error.html", message="Sorting error."), 500

    return render_template("index.html", wanted=items)

@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", message="Page not found."), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", message="Server error occurred."), 500

if __name__ == "__main__":
    app.run(debug=True)

