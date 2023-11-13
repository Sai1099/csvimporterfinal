from flask import Flask, render_template, request
import pandas as pd
import os
import uuid
from pymongo import MongoClient

app = Flask(__name__)
def generate_collection_name():
    return 'uploaded_data_' + str(uuid.uuid4())



@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', message='No file provided.')

        file = request.files['file']

        # Check if the file is not empty
        if file.filename == '':
            return render_template('index.html', message='No file selected.')

        # Check if the file is a CSV file
        if file.filename.endswith('.csv'):
            try:
                # Load the CSV file into a DataFrame
                df = pd.read_csv(file)
                
                collection_name = generate_collection_name()
             # Connect to MongoDB
                client = MongoClient('mongodb://localhost:27017')
                db = client['sai']
                collection = db[collection_name] 

                # Convert DataFrame to a list of dictionaries (one dictionary per row)
                data = df.to_dict(orient='records')

                # Insert the data into MongoDB
                collection.insert_many(data)

                # Fetch the uploaded data from MongoDB
                uploaded_data = list(collection.find())

                # Close the MongoDB connection
                client.close()

                return render_template('index.html', uploaded_data=uploaded_data, message='File uploaded and processed successfully!')

            except pd.errors.EmptyDataError:
                return render_template('index.html', message='Error reading CSV file. Please make sure it is not empty.')

        else:
            return render_template('index.html', message='Invalid file format. Please upload a CSV file.')
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
