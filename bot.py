import asyncio
from telegram import Bot
import os
import requests

# Load secrets from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
HOLLYWOOD_CHANNEL = os.getenv("HOLLYWOOD_CHANNEL")
TOLLYWOOD_CHANNEL = os.getenv("TOLLYWOOD_CHANNEL")
BOLLYWOOD_CHANNEL = os.getenv("BOLLYWOOD_CHANNEL")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

bot = Bot(token=BOT_TOKEN)

# Function to get movie details from TMDB
def get_movie_details(movie_name, category="hollywood"):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    response = requests.get(url).json()
    if response["results"]:
        movie = response["results"][0]
        title = movie.get("title")
        release_date = movie.get("release_date")
        overview = movie.get("overview")
        poster_path = movie.get("poster_path")
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None
        return {"title": title, "release_date": release_date, "overview": overview, "poster": poster_url}
    return None

# Async function to post movie in a channel
async def post_movie(channel, movie_name):
    movie = get_movie_details(movie_name)
    if not movie:
        return
    caption = f"*{movie['title']}* ({movie['release_date']})\n\n{movie['overview']}\n\n[Watch Here](https://www.themoviedb.org/movie/{movie_name.replace(' ', '-')})"
    
    if movie["poster"]:
        await bot.send_photo(chat_id=channel, photo=movie["poster"], caption=caption, parse_mode="Markdown")
    else:
        await bot.send_message(chat_id=channel, text=caption, parse_mode="Markdown")

# Example: Auto-post for testing
async def main():
    await post_movie(HOLLYWOOD_CHANNEL, "Inception")
    await post_movie(TOLLYWOOD_CHANNEL, "Pushpa")
    await post_movie(BOLLYWOOD_CHANNEL, "Pathaan")

if __name__ == "__main__":
    asyncio.run(main())
