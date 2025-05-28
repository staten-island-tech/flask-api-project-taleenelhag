from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def fetch_fbi_data():
    """Fetch FBI data, return empty list on error."""
    url = "https://api.fbi.gov/wanted/v1/list"
    try:
        response = requests.get(url, params={"page": 2})
        response.raise_for_status()
        return response.json().get("items", [])
    except:
        return []

@app.route("/")
def index():
    query = request.args.get("query", "").strip().lower()
    items = fetch_fbi_data()
    if query:
        items = [item for item in items if query in item.get("title", "").lower() or query in item.get("details", "").lower()]
    return render_template("index.html", wanted=items, query=query)

@app.route("/wanted/<uid>")
def wanted_detail(uid):
    items = fetch_fbi_data()
    person = next((p for p in items if p.get("uid") == uid), None)
    if not person:
        return f"<h1>Person not found</h1><p><a href='/'>Back to list</a></p>", 404
    return render_template("wanted.html", person=person)

@app.route("/sort/<key>")
def sort_by(key):
    query = request.args.get("query", "").strip().lower()
    items = fetch_fbi_data()
    if query:
        items = [item for item in items if query in item.get("title", "").lower() or query in item.get("details", "").lower()]
    if key == "title":
        items.sort(key=lambda x: x.get("title", ""))
    elif key == "reward":
        items.sort(key=lambda x: x.get("reward_text", ""))
    elif key == "publication":
        items.sort(key=lambda x: x.get("publication", ""))
    return render_template("index.html", wanted=items, query=query)

if __name__ == "__main__":
    app.run(debug=True)


