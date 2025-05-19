from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    response = requests.get("https://api.fbi.gov/wanted/v1/list?page=2")
    data = response.json()

    wanted_list = data.get("items", [])  
    return render_template("index.html", wanted=wanted_list)

@app.route("/wanted/<uid>")
def wanted_detail(uid):
    response = requests.get(f"https://api.fbi.gov/wanted/v1/list?page=2{uid}")
    data = response.json()

    return render_template("wanted.html", person=data)

if __name__ == '__main__':
    app.run(debug=True)
