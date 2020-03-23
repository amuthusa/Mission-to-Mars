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
    hemisphere = mongo.db.hemisphere.find_one()
    return render_template("index.html", mars=mars, hem=hemisphere)


@app.route("/Scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = Scraping.scrape_all()
    document_id = mars.update({}, mars_data, upsert=True)
    print(f"updated document id: {document_id}")
    hemisphere = mongo.db.hemisphere
    hemisphere_data = Scraping.scrape_allhemispheres()
    print(f"all hemispheres data: {hemisphere_data}")
    hemisphere.update({}, hemisphere_data, upsert=True)
    return "Scraping successful!"

if __name__ == "__main__":
    app.run()