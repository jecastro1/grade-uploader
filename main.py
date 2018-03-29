import logging

from grade_uploader.uploader import Uploader

if __name__ == '__main__':
    token = ''  # Github API token
    key_path = ''  # Path where the Google API key is stored

    repo = ''  # Repository name

    logging.basicConfig(level=logging.DEBUG)

    uploader = Uploader(repo, token, key_path)
    uploader.upload_grades()
