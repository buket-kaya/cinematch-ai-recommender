import requests
import os
import time # Hızlı istek atıp engellenmeyelim diye ekledik
from dotenv import load_dotenv
from core.models import Movie 

load_dotenv()

class TMDBClient:
    def __init__(self):
        self.api_key = os.getenv('TMDB_API_KEY')
        self.base_url = "https://api.themoviedb.org/3"

    def get_top_rated_movies(self):
        endpoint = f"{self.base_url}/movie/top_rated"
        all_movies = []
        
        # --- BURAYI DEĞİŞTİRDİK (26 yaptık) ---
        target_pages = 26 
        print(f"Veriler çekilmeye başlanıyor (Toplam {target_pages-1} sayfa)...")

        for page_number in range(1, target_pages):
            
            params = {
                "api_key": self.api_key,
                "language": "en-US",
                "page": page_number
            }
            
            response = requests.get(endpoint, params=params)
            
            if response.status_code == 200:
                raw_data = response.json()['results']
                
                for item in raw_data:
                    movie = Movie(
                        id=item['id'],
                        title=item['title'],
                        overview=item['overview'],
                        release_date=item.get('release_date', 'Bilinmiyor'),
                        vote_average=item['vote_average'],
                        poster_path=item.get('poster_path')
                    )
                    all_movies.append(movie)
                
                print(f"Sayfa {page_number} tamamlandı. ({len(all_movies)} film)")
                
            else:
                print(f"Hata (Sayfa {page_number}): {response.status_code}")
            
            # Site bizi robot sanıp engellemesin diye her sayfada 0.2 saniye nefes alıyoruz
            time.sleep(0.2) 
        
        return all_movies

if __name__ == "__main__":
    client = TMDBClient()
    filmler = client.get_top_rated_movies()
    print("-" * 30)
    print(f"TOPLAM ÇEKİLEN FİLM SAYISI: {len(filmler)}")
