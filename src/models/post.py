from uuid import uuid4
from datetime import datetime

from database import Database

__author__ = "prabin bernard"


class Post(object):
    def __init__(self, author, title, content, blog_id, created_date=datetime.utcnow(), id=None, ):
        self.author = author
        self.title = title
        self.content = content
        self.created_date = created_date
        self.blog_id = blog_id
        if id is None:
            self.id = uuid4().hex
        else:
            self.id = id

    def json(self):
        return {
            "author": self.author,
            "title": self.title,
            "content": self.content,
            "created_date": self.created_date,
            "blog_id": self.blog_id,
            "id": self.id
        }

    def save_to_db(self):
        Database.insert(collection='posts', data=self.json())

    @staticmethod
    def from_blog(blog_id):
        return [post for post in Database.find(collection='posts', query={"blog_id": blog_id})]

    def __str__(self):
        return "author: {}, title: {}, content: {}, created_date: {}, blog_id: {}, id: {}".format(
            self.author,
            self.title,
            self.content,
            self.created_date,
            self.blog_id,
            self.id
        )
