from uploader import Uploader
import logging

if __name__ == '__main__':
    token = ''  # Github API token
    repo = ''  # Repository name
    key_path = ''  # Path where the Google API key is stored

    logging.basicConfig(level=logging.DEBUG)

    uploader = Uploader(repo, token, key_path)
    uploader.upload_grades()
