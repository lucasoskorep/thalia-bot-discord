import peewee
from peewee import *

# username =
# password =
mysql_db = MySQLDatabase('discord_thalia_bot', user='root', password='Lo319319',
                         host='Crystal-chaos', port=3306)

class Book(peewee.Model):
    author = peewee.CharField()
    title = peewee.TextField()

    class Meta:
        database = mysql_db

Book.create_table()
book = Book(author="me", title='Peewee is cool')
book.save()

for book in Book.filter(author="me"):
    print(book, book.author, book.title)