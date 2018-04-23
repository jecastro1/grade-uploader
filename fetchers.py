import json
import re
from os.path import join

from grade_uploader.wrappers import Github

REGEX_ITEM_GRADES = '(?:\s*)(\w+)(?:\s*\|\s*)(\d\.\d+)(?:\s*)'
REGEX_FINAL_GRADE = '(?:\\*\\*)(\\d\\.?\\d*)(?:\\*\\*)'
ORG = 'IIC2233'


class GradesFetcher:
    def __init__(self, activity, student_db, token):
        self.github = Github(ORG, activity, token)
        self.student_db = student_db
        self._data = None
        self._users = None

    def _get_user_section(self, username):
        user_file = "{}.json".format(username)
        with open(join(self.student_db, user_file), 'r') as file:
            return json.loads(file.read())['section']

    def _get_user_folder(self, username):
        return 'Correccion/{}/FEEDBACK.md'.format(username)

    def _get_data(self, username):
        feedback = self.github.download_text(self._get_user_folder(username))
        data = {
            x: float(y)
            for x, y in re.findall(REGEX_ITEM_GRADES, feedback)
        }
        data['Nota'] = float(re.findall(REGEX_FINAL_GRADE, feedback)[0])
        data['Sección'] = self._get_user_section(username)
        return data

    @property
    def users(self):
        if self._users is None:
            self._users = self.github.get_directories('Correccion')
        return self._users

    @property
    def data(self):
        if self._data is None:
            self._data = [self._get_data(user) for user in self.users]
        return self._data
