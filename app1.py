import streamlit as st
import pandas as pd
import requests
import pickle
import io
import re   

st.set_page_config(layout="wide")
# Load TMDB API key from Streamlit secrets
try:
    api_key = st.secrets["TMDB_API_KEY"]
except KeyError:
    st.error("TMDB API Key not found. Please set it in your Streamlit secrets.")
    st.stop()

COSINE_SIM_URL = "https://huggingface.co/datasets/royanK16/movie_recommendation/resolve/main/cosine_sim.pkl?download=true"
MOVIE_DATA_URL = "https://huggingface.co/datasets/royanK16/movie_recommendation/resolve/main/movie_data.pkl?download=true"

# Use st.cache_data to load the large data files only once.
@st.cache_data

def load_data_from_url():
    try:
        # Download movie_data.pkl
        st.info("Downloading movie data. This may take a moment...")
        response_data = requests.get(MOVIE_DATA_URL)
        response_data.raise_for_status()  # Check for bad status codes
        final_data = pickle.load(io.BytesIO(response_data.content))

        # Download cosine_sim.pkl
        st.info("Downloading similarity matrix...")
        response_sim = requests.get(COSINE_SIM_URL)
        response_sim.raise_for_status()
        cosine_sim = pickle.load(io.BytesIO(response_sim.content))

        st.success("Data loaded successfully!")
        return final_data, cosine_sim
    except requests.exceptions.RequestException as e:
        st.error(f"Error: Failed to download data from the URL. Please check the URLs.")
        st.error(f"Details: {e}")
        return None, None
    except pickle.UnpicklingError:
        st.error("Error: The downloaded file is not a valid pickle file.")
        return None, None

final_data, cosine_sim = load_data_from_url()

# Only proceed if data was loaded successfully
if final_data is not None:
    class RecommendationsSystems:
        def __init__(self, df, cosine_sim):
            self.df = df
            self.cosine_sim = cosine_sim

        def recommendation_movie(self, Film_title, total_result=5, threshold=0.2):
            idx = self.find_movies(Film_title)
            
            if (idx == -1):
                return []  # Single list is sufficient

            sim_df = self.df.copy()
            sim_df['similarity'] = self.cosine_sim[idx]
            sort_df = sim_df.sort_values(by='similarity', ascending=False)[1:total_result + 1]
            sort_df = sort_df[sort_df['similarity'] >= threshold]

            recommendation_movie = []
            for _, row in sort_df.iterrows(): 
                recommendation_movie.append(row.to_dict()) 

            return recommendation_movie

        def find_movies(self, movie_name):
            for index, title in enumerate(self.df['Film_title']):
              if re.search(movie_name, title, re.IGNORECASE):
                return index
            return -1

    
    # Function to fetch movie poster using TMDB API
    def fetch_poster(movie_title):
        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_title}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
                
            if data['results']:
                # The first result should be the most relevant
                poster_path = data['results'][0].get('poster_path')
                if poster_path:
                    # Construct the full poster URL
                    return f"https://image.tmdb.org/t/p/w500{poster_path}"
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching poster: {e}")
            
        return "https://placehold.co/500x750/cccccc/333333?text=No+Poster"

    RS = RecommendationsSystems(final_data, cosine_sim)

    # Streamlit app layout
    st.title("Movie Recommendation System")

    # Dropdown menu to select a movie. Streamlit's selectbox supports typing to filter the list.
    movies = st.selectbox(
        "Select a movie:", 
        final_data['Film_title'].values,
    )

    if st.button("Get Recommendations"):
        with st.spinner('Fetching recommendations...'):
            recommendations = RS.recommendation_movie(movies, total_result=10, threshold=0.2)
                
            # The recommendation_movie function now returns a list of dictionaries.
            if recommendations:
                st.subheader(f"Top 10 Movie Recommendations for {movies}:")
                num_columns = 5
                        
                for i in range(0, len(recommendations), num_columns):
                    cols = st.columns(num_columns)
                            
                    for j in range(num_columns):
                        if i + j < len(recommendations):
                            movie_info = recommendations[i + j]
                            movie_title = movie_info['Film_title']
                            poster_url = fetch_poster(movie_title)
                                    
                            with cols[j]:
                                st.image(poster_url, use_container_width=True)
                                st.caption(movie_title)
            else:
                st.info("No recommendations found for this movie. Please try a different title.")
