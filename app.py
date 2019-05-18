from flask import Flask, render_template
from pymongo import MongoClient
client = MongoClient("localhost", 27017)
mars_db = client.mars_db.mars_collection
mars_data =  list(mars_db.find())
for row in mars_data:
    print(row)
fact_list = []
for x in row["facts"]:
    fact_list.append(row["facts"][x])
row["facts"] = fact_list

app = Flask(__name__)
@app.route("/")
def home():
    return  render_template ( "index.html" )
@app.route("/scrape.html")
def page2():
    return render_template("scrape.html", mars_data = row)

if __name__ == "__main__":
    app.run(debug=True)
