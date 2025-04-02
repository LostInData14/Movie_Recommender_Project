import pickle
import streamlit as st
import requests
from dotenv import load_dotenv
import os
import gdown


load_dotenv()
api_key = os.getenv("API_KEY")

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    data = requests.get(url)
    data = data.json()
    # poster_path = data['poster_path']
    # full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    # return full_path
    if 'poster_path' in data and data['poster_path']:
         poster_path = data['poster_path']
         full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    else:
         full_path = "https://via.placeholder.com/500x750?text=No+Image"
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')


# Define the project folder path
project_folder = "C:/Users/kruti/OneDrive/Desktop/LostInData/Projects/Movie_Recommender_System/Recommender_Project"

# Google Drive file links
movies_url = "https://drive.google.com/uc?id=1gwYBndELnPt54PDBiVFr8izlfy0KRHWY"
similarity_url = "https://drive.google.com/uc?id=1MhRfkdz-bze3BrirmcqIC0n_qsklaSRP"

# Ensure the folder exists
os.makedirs(project_folder, exist_ok=True)

# Download files into the project folder
movies_path = os.path.join(project_folder, "movies.pkl")
similarity_path = os.path.join(project_folder, "similarity.pkl")

# Download files
gdown.download(movies_url, movies_path, quiet=False)
gdown.download(similarity_url, similarity_path, quiet=False)


# Load the files
with open('movies.pkl', 'rb') as f:
    movies = pickle.load(f)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

    # Dropdown for movie selection
    movie_list = movies['title'].values
    selected_movie = st.selectbox(
        "Type or select a movie from the dropdown",
        movie_list
    )

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
