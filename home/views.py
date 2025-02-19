from django.shortcuts import render,HttpResponse
import requests
# Create your views here.
def index(request):
    return render(request,'index.html')



# model
import pickle
rec=pickle.load(open(r'model/movie_list1.pkl','rb'))
sim=pickle.load(open(r'model/indices.pkl','rb'))



# Function to get movie poster URL from OMDb API

# Function to get movie poster URL from OMDb API
def poster(id):
    try:
        res = requests.get(f'https://www.omdbapi.com/?i={id}&apikey=d7a5ccec', timeout=5)
        res.raise_for_status()  # Raise error for bad responses (4xx, 5xx)
        data = res.json()
        
        # Check if poster exists in response
        return data.get("Poster", "https://via.placeholder.com/300x450?text=No+Image")  
    except requests.exceptions.RequestException as e:
        print(f"Error fetching poster for {id}: {e}")
        return "https://via.placeholder.com/300x450?text=Error"  # Fallback image


# # Function to recommend movies
# def recommend(movie):
#     if movie not in rec['movie_name'].values:
#         print(f"Movie '{movie}' not found!")
#         return []  # Return an empty list if movie is not found
    
#     index = rec[rec['movie_name'] == movie].index[0]
#     distances = sorted(list(enumerate(sim[index])), reverse=True, key=lambda x: x[1])
    
#     recommendations = []
#     for i in distances[1:6]:
#         recommended_movie_name = rec.iloc[i[0]]['movie_name']
#         movie_id = rec.iloc[i[0]]['movie_id']  # Assuming you have movie ID in the dataset
#         movie_poster = poster(movie_id)  # Get poster for each recommended movie
#         recommendations.append({
#             'name': recommended_movie_name,
#             'poster': movie_poster
#         })
    
#     return recommendations











# # Function to recommend movies
# def recommend(movie, rec, sim):
#     # Convert movie names to lowercase for case-insensitive matching
#     movie = movie.lower()
#     rec['movie_name_lower'] = rec['movie_name'].str.lower()

#     # Check if the movie exists in the dataset
#     if movie not in rec['movie_name_lower'].unique():
#         # Find the closest matching movie name
#         from thefuzz import process
#         closest_match, score = process.extractOne(movie, rec['movie_name_lower'].unique())
#         if score >= 60:  # Adjust threshold as needed
#             print(f"Did you mean '{closest_match}'? Showing results for it.")
#             movie = closest_match
#         else:
#             return f"Movie '{movie}' not found! No similar match found."

#     # Get the index of the movie
#     index = rec[rec['movie_name_lower'] == movie].index[0]

#     # Sort movies based on similarity scores
#     distances = sorted(enumerate(sim[index]), key=lambda x: x[1], reverse=True)

#     # Extract top 5 recommendations (excluding the input movie itself)
#     recommendations = []
#     for i in distances[1:6]:
#         recommended_movie_name = rec.iloc[i[0]]['movie_name']
#         movie_id = rec.iloc[i[0]]['movie_id']  # Assuming you have movie ID in the dataset
#         movie_poster = poster(movie_id)  # Assuming you have a 'poster' function to get movie posters
#         recommendations.append({
#             'name': recommended_movie_name,
#             'poster': movie_poster
#         })
    
#     return recommendations

# Example usage:
# recommendations = recommend("omg 2", rec, sim)
# print(recommendations)


# Example usage:
# recommendations = recommend("omg 2", new, similarity)
# print(recommendations)




from thefuzz import process

# Function to recommend movies
def recommend(movie, rec, indices):
    # Convert movie names to lowercase for case-insensitive matching
    movie = movie.lower()
    rec['movie_name_lower'] = rec['movie_name'].str.lower()

    # Check if the movie exists in the dataset
    if movie not in rec['movie_name_lower'].unique():
        # Find the closest matching movie name
        closest_match, score = process.extractOne(movie, rec['movie_name_lower'].unique())
        if score >= 60:  # Adjust threshold as needed
            print(f"Did you mean '{closest_match}'? Showing results for it.")
            movie = closest_match
        else:
            return f"Movie '{movie}' not found! No similar match found."

    # Get the index of the movie
    index = rec[rec['movie_name_lower'] == movie].index[0]

    # Retrieve top-5 similar movie indices (excluding itself)
    recommended_indices = indices[index][1:6]  # Skip the first one (itself)

    # Extract recommendations
    recommendations = []
    for i in recommended_indices:
        recommended_movie_name = rec.iloc[i]['movie_name']
        movie_id = rec.iloc[i]['movie_id']  # Assuming you have a movie ID column
        movie_poster = poster(movie_id)  # Assuming a 'poster' function to fetch posters
        recommendations.append({
            'name': recommended_movie_name,
            'poster': movie_poster
        })
    
    return recommendations



























# Function to handle search and show recommendations
def search_movie(request):
    query = request.GET.get('query')  # Get the search query from GET
    if query:  # If there's a query
        recommended_movies = recommend(query,rec,sim) 
        print(recommended_movies)
        # Get recommendations based on the query
    else:
        recommended_movies = []  # If no query, return an empty list
    
    # Return the response with recommended movies or an empty list
    return render(request, 'index.html', {'recommended_movies': recommended_movies})