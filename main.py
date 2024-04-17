from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

CLIENT_ID=os.environ.get("SPOTIPY_CLIENT_ID")
CLIENT_SECRET= os.environ.get("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI=os.environ.get("SPOTIPY_REDIRECT_URI")

# Input BillBoard Date
date = input("Which year do you want to travel to?Type the date in this format YYYY-MM-DD:")

# Scrape Top 100 BillBoard page
response=requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
top_100_webpage=response.text

soup=BeautifulSoup(top_100_webpage,"html.parser")
songs=soup.find_all(name="h3",id="title-of-a-story",class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")
songs.insert(0,soup.find(name="h3",id="title-of-a-story",class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet"))

# Get song titles
song_titles=[song.getText().strip() for song in songs]

# Authenticate app
scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
user_id=sp.current_user()['id']

# Retrieve corresponding song uris
song_uris=[]
for song in song_titles:
    results=sp.search(q=f"track:{song} year:{date[:4]}",type="track")
    try:
        uri=results["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} cannot be found.Skipped")

# Create playlist and add Top 100 tracks
playlist=sp.user_playlist_create(user=user_id,name=f"{date} BillBoard 100",public=False)
playlist_id=playlist["id"]
sp.playlist_add_items(playlist_id=playlist_id,items=song_uris)





