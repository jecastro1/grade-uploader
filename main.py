from uploader import Uploader
import logging

if __name__ == '__main__':
    token = 'acc76e06955377e056cf2e0cf9c74e98fa7c5798'  # Github API token
    key_path = 'google_keys.json'  # Path where the Google API key is stored

    repo = 'AC07'  # Repository name

    logging.basicConfig(level=logging.DEBUG)

    uploader = Uploader(repo, token, key_path)
    uploader.upload_grades()
