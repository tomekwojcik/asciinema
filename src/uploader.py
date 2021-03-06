import json
import bz2

from urllib_http_adapter import UrllibHttpAdapter


class File(object):

    def __init__(self, name, content):
        self.name = name
        self.content = content


class Uploader(object):

    def __init__(self, http_adapter=None):
        self.http_adapter = http_adapter if http_adapter is not None else UrllibHttpAdapter()

    def upload(self, api_url, user_token, asciicast):
        url = '%s/api/asciicasts' % api_url
        files  = self._asciicast_files(asciicast, user_token)

        status, headers, body = self.http_adapter.post(url, files=files)

        return body

    def _asciicast_files(self, asciicast, user_token):
        return {
            'asciicast[stdout]': self._stdout_data_file(asciicast.stdout),
            'asciicast[stdout_timing]': self._stdout_timing_file(asciicast.stdout),
            'asciicast[meta]': self._meta_file(asciicast, user_token)
        }

    def _stdout_data_file(self, stdout):
        return File('stdout', bz2.compress(stdout.data))

    def _stdout_timing_file(self, stdout):
        return File('stdout.time', bz2.compress(str(stdout.timing)))

    def _meta_file(self, asciicast, user_token):
        return File('meta.json', self._meta_json(asciicast, user_token))

    def _meta_json(self, asciicast, user_token):
        meta_data = asciicast.meta_data()
        auth_data = { 'user_token': user_token }
        data = dict(meta_data.items() + auth_data.items())

        return json.dumps(data)
