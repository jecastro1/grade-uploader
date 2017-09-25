from wrappers import Github, Google
import re
import logging


class Uploader:
    def __init__(self, repo, token, key_path):
        self.repo = repo
        self.github = Github('IIC2233', repo, token)
        self.google = Google(key_path)
        self.worksheet = self.google.get_worksheet('Notas IIC2233 - Privado', 0)

    def get_github_usernames(self):
        # Github places directories beginning with an uppercase letter before
        # the ones beginning a lowercase letter, so the list is sorted
        usernames = self.github.get_directories('Correccion')
        usernames.sort(key=lambda x: x.lower())
        return usernames

    def get_github_grade(self, username):
        feedback = self.github.download_text('Correccion/{}/FEEDBACK.md'.format(
            username))
        grade = float(re.findall('(?:\*\*)(\d\.\d)(?:\*\*)', feedback)[0])
        return grade

    def get_sheet_usernames(self):
        column_index = self.get_sheet_column_index('Github')
        usernames = self.worksheet.col_values(column_index)[1:]
        return usernames

    def get_sheet_column_index(self, column_name):
        header = self.worksheet.row_values(1)
        index = header.index(column_name) + 1
        return index

    def upload_grades(self, start_username=None, end_username=None):
        github_usernames = self.get_github_usernames()
        start_index = (github_usernames.index(start_username) if
                       start_username else 0)
        end_index = (github_usernames.index(end_username) if
                     end_username else len(github_usernames)) + 1
        github_usernames = github_usernames[start_index:end_index]

        sheet_usernames = self.get_sheet_usernames()
        sheet_column_index = self.get_sheet_column_index(self.repo)
        grades = []
        for i, username in enumerate(github_usernames):
            logging.debug('{} - {}'.format(i, username))
            grade = self.get_github_grade(username)
            if ' & ' in username:
                username_1, username_2 = username.split(' & ')
                sheet_username_index_1 = sheet_usernames.index(username_1) + 2
                sheet_username_index_2 = sheet_usernames.index(username_2) + 2
                grades.append(((sheet_username_index_1, sheet_column_index),
                               grade))
                grades.append(((sheet_username_index_2, sheet_column_index),
                               grade))
            else:
                sheet_username_index = sheet_usernames.index(username) + 2
                grades.append(((sheet_username_index, sheet_column_index),
                               grade))
        self.google.update_cells(self.worksheet, grades)
