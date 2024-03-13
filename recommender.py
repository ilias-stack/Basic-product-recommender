from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

class Recommender():
    # Rank based recommendation
    @staticmethod
    def top_n_products(final_rating, n, min_interaction):
        #Finding products with minimum number of interactions
        recommendations = final_rating[final_rating['rating_count']>min_interaction]
        
        #Sorting values w.r.t average rating 
        recommendations = recommendations.sort_values('avg_rating',ascending=False)
        
        return recommendations.index[:n]
    
    # defining a function to get similar users
    @staticmethod
    def similar_users(user_index, interactions_matrix):
        similarity = []
        for user in range(0, interactions_matrix.shape[0]):
            
            #finding cosine similarity between the user_id of each user
            sim = cosine_similarity([interactions_matrix.loc[user_index]], [interactions_matrix.loc[user]])
            
            #Appending the user and the corresponding similarity score with user_id as a tuple
            similarity.append((user,sim))
            
        similarity.sort(key=lambda x: x[1], reverse=True)
        most_similar_users = [tup[0] for tup in similarity] # Extract the user from each tuple in the sorted list
        similarity_score = [tup[1] for tup in similarity] # Extracting the similarity score from each tuple in the sorted list
    
        #Remove the original user and its similarity score and keep only other similar users 
        most_similar_users.remove(user_index)
        similarity_score.remove(similarity_score[0])
        
        return most_similar_users, similarity_score
    
    # defining the recommendations function to get recommendations by using the similar users' preferences
    @staticmethod
    def recommendations(user_index, num_of_products, interactions_matrix):
        #Saving similar users using the function similar_users defined above
        most_similar_users = Recommender.similar_users(user_index, interactions_matrix)[0]
        
        #Finding product IDs with which the user_id has interacted
        prod_ids = set(list(interactions_matrix.columns[np.where(interactions_matrix.loc[user_index] > 0)]))
        recommendations = []
        
        observed_interactions = prod_ids.copy()
        for similar_user in most_similar_users:
            if len(recommendations) < num_of_products:
                
                #Finding n products which have been rated by similar users but not by the user_id
                similar_user_prod_ids = set(list(interactions_matrix.columns[np.where(interactions_matrix.loc[similar_user] > 0)]))
                recommendations.extend(list(similar_user_prod_ids.difference(observed_interactions)))
                observed_interactions = observed_interactions.union(similar_user_prod_ids)
            else:
                break
        
        return recommendations[:num_of_products]