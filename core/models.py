class Movie:
    def __init__(self, id, title, overview, release_date, vote_average, poster_path):
        # Burası filmin özellikleri (Attributes)
        self.id = id                    # Filmin kimlik numarası (ID)
        self.title = title              # Adı
        self.overview = overview        # Konusu
        self.release_date = release_date # Çıkış tarihi
        self.vote_average = vote_average # Puanı
        
        # Poster resmi için tam linki oluşturuyoruz
        if poster_path:
            self.poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            self.poster_url = "https://via.placeholder.com/500x750?text=No+Poster"

    def __str__(self):
        # "print(film)" dediğimizde ekranda ne yazsın?
        return f"{self.title} ({self.vote_average})"
