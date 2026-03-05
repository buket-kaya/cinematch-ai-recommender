import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class MovieRecommender:
    def __init__(self, movies_list):
        # 1. ADIM: Gelen film listesini Pandas Tablosuna çeviriyoruz
        data = []
        for movie in movies_list:
            # DÜZELTME BURADA YAPILDI:
            # Sol taraf (Anahtar): 'poster_path' (App.py bunu arıyor)
            # Sağ taraf (Değer): movie.poster_url (Senin modelinde ismi bu)
            data.append({
                'id': movie.id,
                'title': movie.title,
                'overview': movie.overview,
                'poster_path': movie.poster_url,  # <--- İşte sihirli dokunuş burada!
                'vote_average': movie.vote_average
            })
        
        self.df = pd.DataFrame(data)
        
        # Motoru hazırla
        self._prepare_engine()

    def _prepare_engine(self):
        # 2. ADIM: TF-IDF (Metin İşleme)
        tfidf = TfidfVectorizer(stop_words='english')
        
        # Boş özetleri doldur
        self.df['overview'] = self.df['overview'].fillna('')
        
        # Matris oluştur
        tfidf_matrix = tfidf.fit_transform(self.df['overview'])
        
        # 3. ADIM: Cosine Similarity (Benzerlik Hesaplama)
        self.cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        
        # İndeksleme
        self.indices = pd.Series(self.df.index, index=self.df['title']).drop_duplicates()

    def get_recommendations(self, title):
        # Film var mı kontrol et
        if title not in self.indices:
            return []

        # İndeksi bul
        idx = self.indices[title]

        # Benzerlik skorlarını al
        sim_scores = list(enumerate(self.cosine_sim[idx]))

        # Sırala (En yüksek puanlılar)
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # İlk 5 filmi al (0. kendisi olduğu için 1'den 6'ya kadar alıyoruz)
        sim_scores = sim_scores[1:6]

        # İndeksleri listele
        movie_indices = [i[0] for i in sim_scores]
        
        # Sonuçları döndür (Poster yoluyla beraber)
        return self.df.iloc[movie_indices][['title', 'poster_path', 'vote_average']].to_dict('records')
