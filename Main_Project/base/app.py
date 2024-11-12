from flask import Flask, render_template, request
import joblib
import numpy as np
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import certifi
ca = certifi.where()

# Create the Flask app
app = Flask(__name__)

# Load trained models and scaler
svm_model = joblib.load('D:\\Study\\6th sem mini project\\mini project\\Main_Project\\model\\svm.pkl')
# Function to perform MongoDB connection and insert a document
# Render the home page
@app.route('/')
def home():
    return render_template('index.html')

def mongoConnection(request_data):
    client = MongoClient(
        "mongodb+srv://shripadbhople26:lQAKoIwJ7cYaJdT8@cluster0.xrvzcpe.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        tlsCAFile=ca
    )
    db = client["user_database"]
    collection = db["user_collection"]
    try:
        # Insert a document into the collection
        document = {
            'profile_name': request_data['profile_pic'],
            'noalpha_user': request_data['fullname_word'],
            'description': request_data['description'],
            'private': request_data['private'],
            'posts': request_data['posts'],
            'followers': request_data['followers'],
            'follows': request_data['follows'],
        }
        result = collection.insert_one(document)
        print("Inserted document ID:", result.inserted_id)
    except PyMongoError as e:
        print(e)
    finally:
        client.close()

@app.route('/form', methods=['POST'])
def predict_and_insert():
    request_data = request.form
    # Insert data into MongoDB
    mongoConnection(request_data)
    # Perform prediction
    return predict()

# Perform prediction
def predict():
    # Get input data from the form
    profile_pic = int(request.form['profile_pic'])
    fullname_word = int(request.form['fullname_word'])
    description = int(request.form['description'])
    private = int(request.form['private'])
    posts = int(request.form['posts'])
    followers = int(request.form['followers'])
    follows = int(request.form['follows'])

    # Scale the input data
    input_data = np.array([profile_pic, fullname_word, description, private, posts, followers, follows]).reshape(1, -1)

    # Perform prediction
    is_fake = svm_model.predict(input_data)
    if is_fake:
        return render_template('prediction.html', prediction='FAKE')
    else:
        return render_template('prediction.html', prediction="REAL")

# Run the Flask app
if __name__ == '__main__':
    # Connect to MongoDB and insert a document
    # Run the Flask app
    app.run(debug=True)