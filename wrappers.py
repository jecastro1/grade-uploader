import requests


class Github:
    def __init__(self, user, repo, token):
        self.user = user
        self.repo = repo
        self.auth = (user, token)

        self.url = 'https://api.github.com/repos/{}/{}/contents'.format(
            self.user, self.repo)

    def get_file_text(self, path):
        url = '{}/{}'.format(self.url, path)
        response = requests.get(url, auth=self.auth)
        response_json = response.json()
        download_url = response_json['download_url']
        download_response = requests.get(download_url, auth=self.auth)
        return download_response.text
