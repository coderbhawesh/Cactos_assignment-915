from requests import get
from requests import post
import json
import base64
import requests




def get_token():
    client_id = "1234";
    client_secret = "5678";
    
    auth_string = client_id + ":" + client_secret
    auth_byte = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_byte), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {"grant_type":"client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

token1 = get_token()
print(token1)
    
    
    
def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={name}&type=artist&limit=1"
    
    query_url = url + query 
    
    print(query_url)
    
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    print(json_result)
    

    
    
search_for_artist(token1,"ACDC")

def get_followed_artists(access_token):
    url = "https://api.spotify.com/v1/me/following?type=artist"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    artists = data.get("artists", {}).get("items", [])
    artist_names = [artist["name"] for artist in artists]

    return artist_names
    
print(get_followed_artists(token1))
    
    
def play_top_track(access_token, track_index=0):
    # Get user's top 10 tracks
    top_tracks_url = "https://api.spotify.com/v1/me/top/tracks"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(top_tracks_url, headers=headers)
    data = response.json()
    tracks = data.get("items", [])

    if not tracks:
        return "No top tracks found."

    if track_index >= len(tracks):
        return "Invalid track index."

    track_uri = tracks[track_index]["uri"]

    # Start playback
    play_url = "https://api.spotify.com/v1/me/player/play"
    play_data = {
        "uris": [track_uri]
    }

    play_response = requests.put(play_url, headers=headers, json=play_data)

    if play_response.status_code == 204:
        return f"Playing track: {tracks[track_index]['name']} by {tracks[track_index]['artists'][0]['name']}"
    else:
        return f"Failed to play track: {play_response.status_code} - {play_response.text}"
    
def stop_playback(access_token):
    url = "https://api.spotify.com/v1/me/player/pause"
    headers  = get_auth_header(access_token)

    response = requests.put(url, headers=headers)
    if response.status_code == 204:
        return "Playback stopped."
    else:
        return f"Failed to stop playback: {response.status_code} - {response.text}"


print(play_top_track(token1))

print(stop_playback(token1))