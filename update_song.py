import requests
import datetime
import os

def get_token():
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": os.environ["SPOTIFY_REFRESH_TOKEN"],
        "client_id": os.environ["SPOTIFY_CLIENT_ID"],
        "client_secret": os.environ["SPOTIFY_CLIENT_SECRET"],
    }
    r = requests.post(url, data=data)
    return r.json()["access_token"]

def get_recent_tracks(token):
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(
        "https://api.spotify.com/v1/me/player/recently-played?limit=50",
        headers=headers
    )
    return r.json()["items"]

def pick_top_song(tracks):
    today = datetime.datetime.now().date()
    counts = {}

    for t in tracks:
        played_at = datetime.datetime.fromisoformat(
            t["played_at"].replace("Z", "+00:00")
        ).date()

        if played_at != today:
            continue

        name = t["track"]["name"]
        counts[name] = counts.get(name, 0) + 1

    if not counts:
        return "No songs played yet today"

    return max(counts, key=counts.get)

token = get_token()
tracks = get_recent_tracks(token)
top_song = pick_top_song(tracks)

with open("TOP_SONG.md", "w") as f:
    f.write(f"### 🎧 Top Song Today\n**{top_song}**\n") 
