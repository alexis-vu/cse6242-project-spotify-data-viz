import spotipy
from spotipy.oauth2 import SpotifyOAuth
import operator

CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
SPOTIPY_REDIRECT_URI = "http://localhost:3000"

scope = "user-top-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI, scope=scope))
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


'''
    Retrieves top artists, tracks, and genres of current user.
    Argument(s):
        time_range - Specifies time range of data (short_term, medium_term, long_term) medium_term by default.
    Return value:
        Dictionary with user's top 5 items in each category.
            keys: artists, tracks, and genres
            values: artist IDs, track IDs, and genres
'''
def get_top_items(time_range: str = "medium_term") -> dict:
    top_artist_res = sp.current_user_top_artists(limit=5, time_range=time_range)
    top_artists_names = [item['name'] for item in top_artist_res['items']]
    top_artists_ids = [item['id'] for item in top_artist_res['items']]

    top_tracks_res = sp.current_user_top_tracks(limit=5, time_range=time_range)
    top_track_names = [item['name'] for item in top_tracks_res['items']]
    top_track_ids = [item['id'] for item in top_tracks_res['items']]

    genres = {}
    for artist in top_artist_res['items']:
        for genre in artist['genres']:
            if genre in genres:
                genres[genre] += 1
            else:
                genres[genre] = 0

    genres = sorted(genres.items(), key=operator.itemgetter(1), reverse=True)[:5]
    top_genres = [item[0] for item in genres]

    return {'artists': top_artists_ids, 'tracks': top_track_ids, 'genres': top_genres}


"""
    Gets recommendations based on user's top artists, tracks, or genres.
    Argument(s):
        seed_type (required): Type of seed to make recommendations on. (artist, track, or genre)
        limit: Limit of number of tracks to recommend. 20 by default.
        time_range - Specifies time range of data (short_term, medium_term, long_term) medium_term by default.
    Return value:
        No return value. Prints out recommended tracks with artist name(s) and album.
"""
def get_recommendations(seed_type: str, limit: int = 20, time_range: str = "medium_term"):
    top_items = get_top_items(time_range=time_range)

    artists = top_items['artists']
    tracks = top_items['tracks']
    genres = top_items['genres']

    recommended_tracks = []

    if seed_type == 'artist':
        recommended_tracks = sp.recommendations(seed_artists=artists, limit=limit)['tracks']
    elif seed_type == 'track':
        recommended_tracks = sp.recommendations(seed_tracks=tracks, limit=limit)['tracks']
    elif seed_type == 'genre':
        recommended_tracks = sp.recommendations(seed_genres=genres, limit=limit)['tracks']

    recommendations = []

    for track in recommended_tracks:
        rec = {'track': track['name'], 'album': track['album']['name']}
        if len(track['album']['artists']) == 1:
            rec['artists'] = track['album']['artists'][0]['name']
        else:
            rec['artists'] = [artist['name'] for artist in track['album']['artists']]

        recommendations.append(rec)

    for idx, item in enumerate(recommendations):
        print(idx, item['track'], "–", item['artists'], "( Album:", item['album'], ")")


if __name__ == "__main__":
    # seed_type values: artist, track, genre,
    # limit: 0-100, default is 20 if not provided
    get_recommendations(seed_type='genre', limit=50)
