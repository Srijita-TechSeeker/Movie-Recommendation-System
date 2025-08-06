
# Movie Recommendation System

This is a movie recommendation system built using Streamlit and TMDB API.

# Movie-Recommendation-System
A movie recommender system built using Streamlit and TMDB API. It suggests top 5 similar movies based on the selected title and displays their posters.

# 🎬 CineMatch - Movie Recommendation System

[CineMatch Live Demo 🚀](https://movie-recommendation-system-qcpntp76dddbex7qok76md.streamlit.app/)

CineMatch is a sleek, content-based movie recommendation system built using Python and Streamlit. It recommends movies similar to your favorites based on movie metadata and similarity scores. The frontend is designed with a stylish gradient interface and a clean, professional layout, ideal for portfolios and resumes.

---

## 📌 Features

- 🎥 **Movie Recommendations** – Get 5 similar movies instantly
- 🖼️ **Poster Previews** – Visualize recommendations with real movie posters
- ⭐ **Metadata Display** – Includes rating, genre, and release year
- 🧠 **Content-Based Filtering** – Uses cosine similarity between movie vectors
- 🧾 **Single Page Web App** – Built with Streamlit and deployed online
- 🖌️ **Modern UI/UX** – Light gradient background, navigation bar, and clean layout

---

## 🔧 Tech Stack

- **Frontend:** Streamlit, HTML/CSS for custom styling
- **Backend:** Python, Pandas, NumPy
- **ML Logic:** Cosine Similarity using Scikit-learn
- **API:** TMDb API (for movie posters and metadata)
- **Deployment:** Streamlit Cloud

---

## 📊 How It Works

1. User selects a movie from the dropdown.
2. The app computes similarity scores based on movie vectors.
3. Top 5 similar movies are displayed with:
   - Title
   - Poster
   - IMDb rating
   - Genre
   - Release year

---

## 📁 Project Structure

├── app.py # Main Streamlit application
├── movie_dict.pkl # Preprocessed movie data (title + id)
├── similarity_compressed.npz # Compressed similarity matrix
├── requirements.txt # Python dependencies
└── README.md # Project overview (you’re here)

