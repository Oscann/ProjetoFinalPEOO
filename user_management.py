import datetime
import os
import pickle

DATA_PATH = "./data.txt"
DEFAULT_USER_DB = dict()


class User:
    def __init__(self, username: str, password: str):
        self.username = username
        self.__password = password

        self.toDoList = []

    def getUsername(self):
        return self.username

    def getPassword(self):
        return self.__password

    def getToDoList(self):
        return self.toDoList

    def __str__(self):
        return self.username


class ToDoItem:
    def __init__(self, text: str, deadline: datetime.datetime = None):
        self.text = text
        self.deadline = deadline
        self.done = False

    def getText(self):
        return self.text

    def getDeadline(self):
        return self.deadline

    def isDone(self):
        return self.done


def getData():
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "xb") as f:
            pickle.dump(DEFAULT_USER_DB, f)
        return DEFAULT_USER_DB

    with open(DATA_PATH, "rb") as f:
        data = pickle.load(f)
    return data


def saveData(data: dict):
    with open(DATA_PATH, "wb") as f:
        pickle.dump(data, f)
