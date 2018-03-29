import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials


class Github:
    def __init__(self, user, repo, token):
        self.user = user
        self.repo = repo
        self.auth = (user, token)

        self.api_url = 'https://api.github.com/repos/{}/{}'.format(
            self.user, self.repo)
        self.raw_url = 'https://raw.githubusercontent.com/{}/{}'.format(
            self.user, self.repo)

    def get_file_text(self, path):
        url = '{}/contents/{}'.format(self.api_url, path)
        response = requests.get(url, auth=self.auth)
        response_json = response.json()
        download_url = response_json['download_url']
        download_response = requests.get(download_url, auth=self.auth)
        return download_response.text

    def get_file(self, path):
        url = '{}/contents/{}'.format(self.api_url, path)
        response = requests.get(url, auth=self.auth)
        response_json = response.json()
        return response_json

    def get_directories(self, path):
        response_json = self.get_file(path)
        if isinstance(response_json, dict):
            raise ValueError('Path entered is not a directory')
        directories = [
            directory['name'] for directory in response_json
            if '.' not in directory['name']
        ]
        return directories

    def download_text(self, path, branch='master'):
        url = '{}/{}/{}'.format(self.raw_url, branch, path)
        response = requests.get(url, auth=self.auth)
        return response.text


class Google:
    def __init__(self, key_path):
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            key_path, scope)
        self.gc = gspread.authorize(credentials)

    def get_worksheet(self, spreadsheet_name, index):
        return self.gc.open(spreadsheet_name).get_worksheet(index)

    @staticmethod
    def update_cells(worksheet, data):
        cells = [worksheet.cell(*element[0]) for element in data]
        for i in range(len(data)):
            cells[i].value = data[i][1]
        worksheet.update_cells(cells)
