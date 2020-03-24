from peewee import *
from datetime import date

db = MySQLDatabase("spider", host = "127.0.0.1", port=3306, user="root",password ="1234")

class Person(Model):
    name = CharField(max_length=20)
    birthday = DateField()

    class Meta:
        database = db # This model uses the "people.db" database.

if __name__ == "__main__":
    db.create_tables([Person])

    # uncle_bob = Person(name = "Bob", birthday = date(1997, 7, 26))
    # uncle_bob.save()
    #
    # uncle_bob = Person(name="Jacky", birthday=date(1991, 1, 22))
    # uncle_bob.save()

    # jacky = Person.get(Person.name == "Jacky")
    # print(jacky.birthday)

    
