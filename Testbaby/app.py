from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from pymongo import MongoClient
from bson import ObjectId
import uuid

app = Flask(__name__)

# Function to generate a random collection name
def generate_collection_name():
    return 'uploaded_data_' + str(uuid.uuid4())

# Connect to MongoDB outside the routes to make sure it's accessible
client = MongoClient('mongodb://localhost:27017')
db = client['sai']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']

        # Check if the file is an Excel file (you may modify this for other formats)
        if file.filename.endswith('.xlsx'):
            # Load the Excel file into a DataFrame
            df = pd.read_excel(file, engine='openpyxl')

            # Generate a random collection name
            collection_name = generate_collection_name()

            # Access the dynamically created collection
            collection = db[collection_name]

            # Convert DataFrame to a list of dictionaries (one dictionary per row)
            data = df.to_dict(orient='records')

            # Insert the data into the dynamically created collection
            collection.insert_many(data)

            # Fetch the uploaded data from the dynamically created collection
            uploaded_data = list(collection.find({}, {'_id': 0}))

            return render_template('display_table.html', uploaded_data=uploaded_data)
        else:
            return render_template('index.html', error='Invalid file format. Please upload an Excel file.')
    else:
        return render_template('index.html')

@app.route('/edit', methods=['GET', 'POST'])
def edit_data():
    if request.method == 'POST':
        # ... (previous code for handling the form submission)

        # Assuming some processing is done here, redirect to another page or return a response
        return redirect(url_for('edit)'))

    else:
        # Fetch the data to be edited from the MongoDB collection
        collection_name = request.args.get('collection_name')
        collection = db[collection_name]
        uploaded_data = list(collection.find({}, {'_id': 1, 'name': 1, 'gmail': 1, 'phno': 1, 'rollno': 1}))

        return render_template('edit.html', uploaded_data=uploaded_data)

if __name__ == '__main__':
    app.run(debug=True)



