from uploader import Uploader

if __name__ == '__main__':
    token = ''  # Github API token
    repo = ''  # Repository name
    key_path = 'google_keys.json'  # Path where the Google API key is stored

    uploader = Uploader(repo, token, key_path)
    uploader.upload_grades()
