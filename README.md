# 🎬 CineMatch: AI-Powered Movie Recommender

CineMatch is a robust movie recommendation system built with Python, leveraging machine learning to provide personalized suggestions based on movie content.

## ✨ Key Features
* **AI-Driven Suggestions:** Uses **TF-IDF Vectorization** and **Cosine Similarity** to match movie overviews.
* **Real-time Data:** Fetches the latest top-rated movies directly from the **TMDB API**.
* **Interactive UI:** Built with **Streamlit** for a seamless and responsive user experience.
* **Smart Data Processing:** Handles 500+ records efficiently using **Pandas**.

## 🛠️ Technology Stack
* **Language:** Python 3.x
* **Data Science:** Scikit-learn, Pandas
* **Web Framework:** Streamlit
* **API Integration:** Requests, TMDB API
* **Environment Management:** Python-dotenv

## ⚙️ Technical Logic
The recommendation engine analyzes movie descriptions and calculates a similarity score between titles. The algorithm complexity for similarity matrix calculation is $O(N^2)$, ensuring high-precision results for the current dataset.
