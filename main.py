from bs4 import BeautifulSoup
import requests
import spotipy

CLIENT_ID = "YOUR CLIENT ID"
CLIENT_SECRET = "YOUR SECRET"
SPOTIPY_REDIRECT_URI = "http://example.com"     # same as in dashboard
USER_ID = "YOUR USER ID"

what_time = input("Which year do you want to travel to? "
                  "Type the date in this format YYYY-MM-DD: ")
YEAR = what_time[0:4]

response = requests.get(f"https://www.billboard.com/charts/hot-100/{what_time}/")
page_with_songs = response.text

soup = BeautifulSoup(page_with_songs, "html.parser")
text = soup.find_all(name="h3", class_=["a-no-trucate",
                                        "u-line-height-125"])
songs_title = [thing.getText().replace("\n", "").replace("\t", "") for thing in text]

oauth_manager = spotipy.oauth2.SpotifyOAuth(scope="playlist-modify-private",
                                            client_id=CLIENT_ID,
                                            client_secret=CLIENT_SECRET,
                                            redirect_uri=SPOTIPY_REDIRECT_URI,)
sp = spotipy.Spotify(oauth_manager=oauth_manager)

playlist = sp.user_playlist_create(user=USER_ID,
                                   name=f"Top 100 songs from {YEAR}",
                                   public=False)
playlist_id = playlist["id"]

song_uris = []
for song in songs_title:
    result = sp.search(q=f"track:{song} year:{YEAR}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)
