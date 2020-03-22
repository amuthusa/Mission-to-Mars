#import flask related dependency
from flask import Flask, render_template
from flask_pymongo import PyMongo
import Scraping

#set flask app
app = Flask(__name__)

#connect to mongodb using pymongo
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/Scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = Scraping.scrape_all()
    mars.update({}, mars_data, upsert=True)
    #mars.insert(mars_data)
    return "Scraping successful!"

if __name__ == "__main__":
    app.run()