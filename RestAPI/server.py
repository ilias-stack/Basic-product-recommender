from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle

import sys
sys.path.append("..")
from constants import *
from recommender import Recommender
import json

# Initialising Flask app
app = Flask(__name__)
CORS(app)

final_rating_data = None
final_ratings_matrix_data = None


# Getting the matrices data and storing them
with open(f"../{FINAL_RATING}","rb") as f:
    final_rating_data = pickle.load(f)
    
with open(f"../{FINAL_RATINGS_MATRIX}","rb") as f:
    final_ratings_matrix_data = pickle.load(f)

@app.route("/",methods = ["GET"])
def working_check():
    return "<h1>Hello</h1>"


# Rank_based recommendation
@app.route('/rank_based', methods=['POST'])
def get_recommendation_rank_based():
    # Getting the request body to fill in recommendation details
    request_body = request.json
    n = int(request_body["n"])
    min_interaction = int(request_body["min_interaction"])
    return jsonify(list(Recommender.top_n_products(final_rating_data,n,min_interaction)))
        

# Collaborative_based recommendation
@app.route('/collaborative_based', methods=['POST'])
def get_recommendation_collaborative_based():
    # Getting the request body to fill in recommendation details
    request_body = request.json
    user_index = int(request_body["user_index"])
    num_of_products = int(request_body["num_of_products"])
    return jsonify(list(Recommender.recommendations(user_index,num_of_products,final_ratings_matrix_data)))

# Running the app if this file is executed directly
if __name__ == '__main__':
    
    app.run(debug=True,port=PORT_NUMBER)