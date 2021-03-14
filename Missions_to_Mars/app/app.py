from flask import Flask, render_template, redirect, url_for
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
import pymongo
import scrape_mars

app = Flask(__name__)

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Connect to mars_app database
db = client.mars_app

@app.route("/")
def index():
    mars = db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping successful!"

if __name__ == "__main__":
    app.run()