from flask import Flask, render_template
import requests

app = Flask(__name__)

# Home page – list of wanted persons
@app.route("/")
def index():
    response = requests.get("https://api.fbi.gov/wanted/v1/list")
    data = response.json()

    wanted_list = data.get("items", [])  # List of wanted individuals
    return render_template("index.html", wanted=wanted_list)

# Detail page for a wanted person
@app.route("/wanted/<uid>")
def wanted_detail(uid):
    response = requests.get(f"https://api.fbi.gov/wanted/v1/list/{uid}")
    data = response.json()

    return render_template("wanted.html", person=data)

if __name__ == '__main__':
    app.run(debug=True)
