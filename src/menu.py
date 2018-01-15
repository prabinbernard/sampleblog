from database import Database
from models.blog import Blog
from models.post import Post

__author__ = "prabin bernard"


class Menu(object):
    def __init__(self):
        # Ask user for an author name
        # check if the user has a blog
        # if not ask them to create one
        self.author = input("Enter your name: ")
        self.user_blog = None
        if self._user_has_account():
            print("Welcome back {}".format(self.author))

        else:
            self._prompt_for_user_account()

    def _user_has_account(self):
        blog = Database.find_one(collection='blogs', query={"author": self.author})
        if blog is not None:
            self.user_blog = Blog.from_mongo(blog['id'])
            return True
        else:
            return False

    def _prompt_for_user_account(self):
        print("You do not seem to have an account with us."
              "Please create a blog to proceed.")
        title = input("Enter the title of the blog:")
        description = input("Enter the description: ")
        blog = Blog(author=self.author, title=title, description=description)
        blog.save_to_db()
        self.user_blog = blog

    def run_menu(self):
        # user read or write blogs
        # if read:
        # list all the blogs in the database
        # allow user to pick one
        # display posts
        # if write:
        # prompt to write a post
        read_or_write = input("Do you want to read(R) or write(W) blogs: ")
        if read_or_write == 'R':
            self._list_blogs()
            self._view_blog_posts()

        elif read_or_write == 'W':
            self.user_blog.new_post()
        else:
            print("Thanks for blogging")

    @staticmethod
    def _list_blogs():
        for blog in Database.find(collection='blogs', query={}):
            print("ID: {}, Title {}, Author:{}".format(blog['id'], blog['title'], blog['author']))

    @staticmethod
    def _view_blog_posts():
        blog_id = input("Enter the id of the blog you want to view: ")
        blog = Blog.from_mongo(blog_id)
        posts = blog.get_posts()
        for post in posts:
            print("Date: {}, Title: {}\n\n{}".format(post['created_date'], post['title'], post['content']))

