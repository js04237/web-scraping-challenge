from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars
import pymongo

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_data
collection = db.scraped_data

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    destination_data = collection.find({}, {"_id": 0})# "latest_article_title": 1})

    # Return template and data
    return render_template("index.html", mars_db=destination_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function
    mars_data = mission_to_mars.scrape_data()
    
    # Drop any old data
    collection.drop()

    # Update the Mongo database using update and upsert=True
    for data in mars_data:
        collection.insert_one(data)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
