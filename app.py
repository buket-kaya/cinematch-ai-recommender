import streamlit as st
import os
from core.api_client import TMDBClient
from core.recommender import MovieRecommender

# Page Configuration
st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS for better looking cards
st.markdown("""
    <style>
    .movie-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Main Title
st.title("🎬 CineMatch: AI-Powered Movie Recommender")
st.markdown("### Discover movies based on what you actually like.")

# Initialize Session State
if 'movies' not in st.session_state:
    st.session_state.movies = []

# --- Sidebar (Settings) ---
st.sidebar.header("Settings")
st.sidebar.write("Click below to fetch the latest top-rated movies.")

if st.sidebar.button("Refresh / Fetch Data"):
    client = TMDBClient()
    with st.spinner("Fetching data from TMDB API... (This might take a moment)"):
        try:
            movies = client.get_top_rated_movies()
            st.session_state.movies = movies
            st.sidebar.success(f"Success! {len(movies)} movies loaded.")
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

# --- Main Area ---

if not st.session_state.movies:
    st.info("👈 Please click the **'Refresh / Fetch Data'** button in the sidebar to start!")
else:
    # 1. Prepare Data for Dropdown
    # Check if items are objects or dicts for the dropdown
    movie_titles = []
    for m in st.session_state.movies:
        if isinstance(m, dict):
            movie_titles.append(m.get('title'))
        else:
            movie_titles.append(m.title)
    
    # 2. User Selection
    selected_movie_name = st.selectbox(
        "Select a movie you liked:",
        movie_titles
    )

    # 3. Recommendation Button
    if st.button("Show Recommendations 🚀"):
        
        recommender = MovieRecommender(st.session_state.movies)
        recommendations = recommender.get_recommendations(selected_movie_name)
        
        if recommendations:
            st.subheader(f"Because you liked '{selected_movie_name}':")
            st.write("---")
            
            # Create columns to display movies side by side
            # We take top 5 recommendations
            top_recommendations = recommendations[:5]
            cols = st.columns(len(top_recommendations))
            
            for idx, movie in enumerate(top_recommendations):
                with cols[idx]:
                    # --- HATA DUZELTME KISMI ---
                    # Gelen verinin tipini (Dict mi Object mi?) kontrol edip ona gore aliyoruz
                    if isinstance(movie, dict):
                        poster_path = movie.get('poster_path')
                        title = movie.get('title')
                        vote = movie.get('vote_average')
                    else:
                        poster_path = getattr(movie, 'poster_path', None)
                        title = getattr(movie, 'title', None)
                        vote = getattr(movie, 'vote_average', None)
                    # ---------------------------

                    if poster_path:
                        full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                        st.image(full_poster_url, use_container_width=True)
                    else:
                        st.write("No Image")
                    
                    st.caption(f"**{title}**")
                    st.write(f"⭐ {vote}")
        else:
            st.warning("Sorry, no recommendations found.")

# Footer
st.markdown("---")
st.caption("CineMatch | Developed by Buket")
