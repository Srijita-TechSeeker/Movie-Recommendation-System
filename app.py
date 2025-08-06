import streamlit as st
import pickle
import pandas as pd
import requests
import numpy as np
import time

# ---------------------- Page Configuration ----------------------
st.set_page_config(page_title="CineMatch - Movie Recommender", layout="wide")

# ---------------------- Load Data ----------------------
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = np.load('similarity_compressed.npz')['similarity']

API_KEY = 'a425ca4774e78c51c7af6657e42236d2'

# ---------------------- CSS Styles ----------------------
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #fce4ec, #f8bbd0, #f48fb1);
        background-attachment: fixed;
        font-family: 'Segoe UI', sans-serif;
    }
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: rgba(255, 255, 255, 0.4);
        padding: 1rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
    }
    .logo {
        font-size: 2rem;
        font-weight: bold;
        color: #ad1457;
    }
    .nav-links {
        display: flex;
        gap: 2rem;
    }
    .nav-link {
        color: #880e4f;
        font-weight: bold;
        font-size: 1.1rem;
        cursor: pointer;
        text-decoration: none;
    }
    .nav-link:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- Navbar with Clickable Links ----------------------
selected_page = st.session_state.get("selected_page", "Home")

navbar_html = f"""
<div class="navbar">
    <div class="logo">🎬 CineMatch</div>
    <div class="nav-links">
        <a class="nav-link" href="?page=Home">Home</a>
        <a class="nav-link" href="?page=About">About</a>
        <a class="nav-link" href="?page=Contact">Contact</a>
    </div>
</div>
"""
st.markdown(navbar_html, unsafe_allow_html=True)

# ---------------------- URL Param Handling ----------------------
query_params = st.query_params
if "page" in query_params:
    selected_page = query_params["page"]
    st.session_state.selected_page = selected_page

# ---------------------- Movie Poster Fetching ----------------------
def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'
        response = requests.get(url)
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    except:
        return "https://via.placeholder.com/500x750.png?text=Image+Not+Available"

# ---------------------- Recommendation Logic ----------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
        time.sleep(0.2)
    return recommended_movies, recommended_posters

# ---------------------- Page Routing ----------------------
if selected_page == "Home":
    st.markdown("<h1>🎬 Welcome to CineMatch</h1>", unsafe_allow_html=True)
    selected_movie = st.selectbox("Choose a movie you like:", movies['title'].values)
    if st.button("🔍 Recommend"):
        names, posters = recommend(selected_movie)
        st.markdown("### 🎯 Top 5 Recommendations")
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.image(posters[i])
                st.caption(names[i])

elif selected_page == "About":
    st.markdown("## 📖 About CineMatch")
    st.write("""
    **CineMatch** is a content-based movie recommendation system that suggests films similar to your favorite ones.

    ### 🔧 Technologies Used:
    - Python, Streamlit
    - Pandas, NumPy
    - Scikit-learn for similarity
    - TMDb API for posters

    It's fast, intuitive, and built for movie lovers.
    """)

elif selected_page == "Contact":
    st.markdown("## 📫 Contact Us")
    st.write("""
    **Developer:** Srijita  
    📧 Email: your.email@example.com  
    🌐 GitHub: [Srijita-TechSeeker](https://github.com/Srijita-TechSeeker)

    Have feedback or want to contribute? Let’s connect!
    """)

