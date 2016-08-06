import requests
import json

class Spotify():
    def __init__(self, client_id, client_secret, callback_uri, scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.callback_uri = callback_uri
        self.scope = scope

    def get_auth_uri(self):
        return "https://accounts.spotify.com/authorize/?client_id=%s&redirect_uri=%s&response_type=%s&scope%s" \
               % (self.client_id, self.callback_uri, "code", self.scope)

    def get_token(self, auth_code):
        data = requests.post(url="https://accounts.spotify.com/api/token",
                             data={
                                 'grant_type': "authorization_code",
                                 'code': auth_code,
                                 'redirect_uri': self.callback_uri,
                                 'client_id': self.client_id,
                                 'client_secret': self.client_secret
                                 },
                             headers={'Authentication': 'Basic'}
                             ).content

        jobj = json.loads(data.decode('utf-8'))

        if 'error' in jobj:
            raise Exception(jobj['error'])
        else:
            return jobj


class SpotifyRequests():
    def __init__(self, access_token, access_token_type):
        self.access_token = access_token
        self.access_token_type = access_token_type

    def make_request(self, url, data=None):
        data = None

        try:
            data = requests.get(
                url=url,
                data=data,
                headers={
                    'Authorization': '%s %s' % (self.access_token_type, self.access_token)
                }
            ).content.decode('utf-8')
        except requests.exceptions.ConnectionError as ce:
            pass
        except:
            raise

        jobj = json.loads(data)

        if 'error' in jobj:
            raise Exception(jobj['error'])
        else:
            return jobj


    def get_my_profile(self):
        return self.make_request("https://api.spotify.com/v1/me")

    def get_playlists(self, userid=None, limit=50, offset=0):
        if userid is None:
            userid = self.get_my_profile()['id']

        return self.make_request(
            "https://api.spotify.com/v1/users/%s/playlists" % userid,
            data={
                limit: limit,
                offset: offset
            }
        )

    def get_playlist_info(self, playlist_id, user_id=None):
        if user_id is None:
            user_id = self.get_my_profile()['id']

        return self.make_request(
            "https://api.spotify.com/v1/users/%s/playlists/%s"
            % (user_id, playlist_id),
        )

    def get_playlist_tracks(self, playlist_id, user_id=None):
        if user_id is None:
            user_id = self.get_my_profile()['id']

        # todo: nie zwraca 100% wyników

        return self.make_request(
            "https://api.spotify.com/v1/users/%s/playlists/%s/tracks"
            % (user_id, playlist_id)
        )