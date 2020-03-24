from peewee import *
from datetime import date

db = MySQLDatabase("spider", host = "127.0.0.1", port=3306, user="root",password ="1234")

class BaseModel(Model):
    class Meta:
        database = db


class Topic(BaseModel):
    title = CharField()
    content = TextField(default="")
    id = IntegerField(primary_key=True)
    author = CharField()
    create_time = DateTimeField()
    answer_nums = IntegerField(default = 0)
    click_nums = IntegerField(default=0)
    praised_nums = IntegerField(default=0)
    jtl = FloatField(default=0.0)
    score = IntegerField(default=0)
    status = CharField()
    last_answer_time = DateTimeField()


class Answer(BaseModel):
    topic_id = IntegerField()
    answer_id = IntegerField(primary_key=True)
    author = CharField()
    content = TextField(default="")
    create_time = DateTimeField()
    praised_nums = IntegerField(default=0)


class Author(BaseModel):
    id = CharField(primary_key=True)
    years = IntegerField(default=0)
    name = CharField()
    description = TextField(null=True)
    blog_nums = IntegerField(default=0)
    resource_nums = IntegerField(default=0)
    forum_nums = IntegerField(default=0)
    blink_nums = IntegerField(default=0)
    column_nums = IntegerField(default=0)
    follower_nums= CharField(default="none")
    following_nums = CharField(default="none")


if __name__ == "__main__":
    db.create_tables([Topic, Answer, Author])