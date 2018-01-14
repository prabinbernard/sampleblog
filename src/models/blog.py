from uuid import uuid4
from datetime import datetime
from database import Database
from models.post import Post

__author__ = "prabin bernard"


class Blog(object):
    def __init__(self, author, title, description, id=None):
        self.author = author,
        self.title = title,
        self.description = description,
        if id is None:
            self.id = uuid4().hex
        else:
            self.id = id

    def json(self):
        return {
            "author": self.author,
            "title": self.title,
            "description": self.description,
            "id": self.id
        }

    def save_to_db(self):
        Database.insert(collection='blogs', data=self.json())

    def __str__(self):
        return "author: {}, title: {}, description: {}, id: {}".format(
            self.author,
            self.title,
            self.description,
            self.id
        )

    def new_post(self):
        title = input("Enter the title of the post: ")
        content = input("Enter the content for the post: ")
        created_date = input("Enter the created date in (DDMMYYY) format or leave blank: ")
        if created_date == "":
            created_date = datetime.utcnow()
        else:
            created_date = datetime.strptime(created_date, "%d%m%Y")

        post = Post(author=self.author,
                    title=title,
                    content=content,
                    created_date=created_date,
                    blog_id=self.id)
        post.save_to_db()

    def get_posts(self):
        return Post.from_blog(blog_id=self.id)

    @classmethod
    def from_mongo(cls, id):
        blog = Database.find_one(collection='blogs', query={"id": id})
        return cls(author=blog['author'],
                   title=blog['title'],
                   description=blog['description'],
                   id=blog['id'])
