import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests


class Google:
    def __init__(self, key_path):
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_path, scope)
        self.gc = gspread.authorize(credentials)

    def get_worksheet(self, spreadsheet_name, index):
        return self.gc.open(spreadsheet_name).get_worksheet(index)


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
