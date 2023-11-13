from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId from bson

app = Flask(__name__)

# Function to generate a random collection name
def generate_collection_name():
    return 'uploaded_data_' + str(uuid.uuid4())

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # ... (previous code for file upload)

        # Fetch the uploaded data from the dynamically created collection
        uploaded_data = list(collection.find({}, {'_id': 0}))

        return render_template('index.html', uploaded_data=uploaded_data, message='File uploaded and processed successfully!')
    else:
        return render_template('index.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit_data():
    if request.method == 'POST':
        # ... (previous code for handling the form submission)

    else:
        # Fetch the data to be edited from the MongoDB collection
        client = MongoClient('mongodb://localhost:27017')
        db = client['sai']
        collection = db['orginalphone']
        uploaded_data = list(collection.find({}, {'_id': 1, 'name': 1, 'gmail': 1, 'phno': 1, 'rollno': 1}))

        return render_template('edit.html', uploaded_data=uploaded_data)

if __name__ == '__main__':
    app.run(debug=True)
