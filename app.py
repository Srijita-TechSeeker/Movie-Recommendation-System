import streamlit as st
import pickle
import pandas as pd
import requests
import time
import numpy as np

# Set page config
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Custom CSS for gradient background and modern design
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #e0f7fa, #ffffff);
    }
    .main {
        background-color: transparent;
    }
    h1 {
        font-size: 3em;
        color: #00796b;
        text-align: center;
        padding: 10px;
    }
    .stButton>button {
        background-color: #00796b;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #004d40;
        transition: 0.3s;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = np.load('similarity_compressed.npz')['similarity']

# TMDb API Key
API_KEY = 'a425ca4774e78c51c7af6657e42236d2'


# Fetch poster from TMDb
def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except Exception:
        return "https://via.placeholder.com/500x750.png?text=Image+Not+Available"


# Recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
        time.sleep(0.3)
    return recommended_movies, recommended_posters


# Movie selector
selected_movie_name = st.selectbox("Choose a movie to get recommendations:", movies['title'].values)

# Button to trigger recommendation
if st.button('🎥 Recommend'):
    names, posters = recommend(selected_movie_name)

    st.markdown("### 📌 Top 5 Recommendations", unsafe_allow_html=True)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(posters[i])
            st.caption(names[i])
