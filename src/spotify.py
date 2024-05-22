# tekore is a wrapper to acces the Spotify Web API
import tekore as tk

from secret import secrets

'/v1/playlists/{playlist_id}/tracks'

client_id  = secrets('Spotifyclient')
client_secret = secrets('SpotifySecret')

app_token = tk.request_client_token(client_id, client_secret)
print(app_token)

spotify = tk.Spotify(app_token)

# conf = (client_id, client_secret, redirect_uri)
# token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)

# spotify = tk.Spotify(token)
# tracks = spotify.current_user_top_tracks(limit=10)
# spotify.playback_start_tracks([t.id for t in tracks.items])