import os
import requests
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

HOLLYWOOD_CHANNEL = os.getenv("HOLLYWOOD_CHANNEL")
TOLLYWOOD_CHANNEL = os.getenv("TOLLYWOOD_CHANNEL")
BOLLYWOOD_CHANNEL = os.getenv("BOLLYWOOD_CHANNEL")

bot = Bot(token=BOT_TOKEN)

def get_movie_details(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    response = requests.get(url).json()

    if response["results"]:
        movie = response["results"][0]
        title = movie["title"]
        release_date = movie.get("release_date", "N/A")
        overview = movie.get("overview", "No description available.")
        rating = movie.get("vote_average", "N/A")
        poster = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None

        return title, release_date, overview, rating, poster
    return None

def get_trailer(movie_name):
    query = f"{movie_name} official trailer"
    return f"https://www.youtube.com/results?search_query={query}"

def post_movie(category, movie_name, watch_link):
    details = get_movie_details(movie_name)
    if not details:
        return

    title, release_date, overview, rating, poster = details
    trailer_link = get_trailer(movie_name)

    caption = f"""
🎬 *{title}*

📅 Release Date: {release_date}
⭐ Rating: {rating}

📝 Overview:
{overview}

▶️ Trailer: {trailer_link}
🎥 Watch Now: {watch_link}
"""

    if category.lower() == "hollywood":
        channel = HOLLYWOOD_CHANNEL
    elif category.lower() == "tollywood":
        channel = TOLLYWOOD_CHANNEL
    elif category.lower() == "bollywood":
        channel = BOLLYWOOD_CHANNEL
    else:
        return

    if poster:
        bot.send_photo(chat_id=channel, photo=poster, caption=caption, parse_mode="Markdown")
    else:
        bot.send_message(chat_id=channel, text=caption, parse_mode="Markdown")

if __name__ == "__main__":
    # Example Auto Post
    post_movie("hollywood", "Inception", "https://example.com/watch-link")
