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
    .movie-meta {
        font-size: 0.85rem;
        color: #4a148c;
        font-weight: 500;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- Navbar ----------------------
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

# ---------------------- Handle Nav Selection ----------------------
query_params = st.query_params
if "page" in query_params:
    selected_page = query_params["page"]
    st.session_state.selected_page = selected_page

# ---------------------- Helper: Fetch Movie Poster & Meta ----------------------
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        res = requests.get(url).json()
        poster = "https://image.tmdb.org/t/p/w500/" + res.get("poster_path", "")
        rating = res.get("vote_average", "N/A")
        year = res.get("release_date", "N/A")[:4]
        genres = ", ".join([g["name"] for g in res.get("genres", [])])
        return poster, rating, year, genres
    except:
        return "https://via.placeholder.com/500x750.png?text=Not+Available", "N/A", "N/A", "N/A"

# ---------------------- Recommend Function ----------------------
def recommend(movie):
    idx = movies[movies['title'] == movie].index[0]
    distances = similarity[idx]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    results = []
    for i in movie_list:
        row = movies.iloc[i[0]]
        poster, rating, year, genres = fetch_movie_details(row.movie_id)
        results.append({
            "title": row.title,
            "poster": poster,
            "rating": rating,
            "year": year,
            "genres": genres
        })
        time.sleep(0.2)
    return results

# ---------------------- Page Logic ----------------------
if selected_page == "Home":
    st.markdown("<h1>🎬 Welcome to CineMatch</h1>", unsafe_allow_html=True)
    selected_movie = st.selectbox("Choose a movie you like:", movies['title'].values)

    if st.button("🔍 Recommend"):
        recs = recommend(selected_movie)
        st.markdown("### 🎯 Top 5 Recommendations")
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.image(recs[i]["poster"])
                st.caption(f"**{recs[i]['title']}**")
                st.markdown(
                    f"<div class='movie-meta'>⭐ {recs[i]['rating']}<br>📅 {recs[i]['year']}<br>🎭 {recs[i]['genres']}</div>",
                    unsafe_allow_html=True
                )

elif selected_page == "About":
    st.markdown("## 📖 About CineMatch")
    st.write("""
    **CineMatch** is a content-based movie recommendation system that helps you discover movies similar to ones you love.

    ### 🔧 Built With:
    - Python & Streamlit
    - Pandas & NumPy
    - Scikit-learn for content similarity
    - TMDb API for movie posters and metadata

    Whether you're a casual viewer or movie buff, CineMatch helps you find your next favorite film 🎥
    """)

elif selected_page == "Contact":
    st.markdown("## 📫 Contact Us")
    st.write("""
    **Developer:** Srijita  
    📧 Email: srijita@example.com  
    🌐 GitHub: [Srijita-TechSeeker](https://github.com/Srijita-TechSeeker)

    Have feedback or suggestions? I'd love to hear from you!
    """)

