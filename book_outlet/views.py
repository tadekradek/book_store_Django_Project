from django.shortcuts import render

# Create your views here.   

#  it is possible to play with the data through the consol, in order to do so, run :
# python manage.py shell
# it opens interactive console 
# in the console itself, we can just simply run python code like:
# from book_outlet.models import Book
# harry_potter = Book() -> standard python syntax, instantiating class
# harry_potter = Book(title="Harry Potter 1 - The Philosopher's Stone", rating = 5) -> this creates an object, but the database was not accessed yet
# only harry_potter.save() -> method taken from inherited classs allows to save the data in database 
# this is equivalent of query inputing something to database in SQL, but here we dont have to do it as Django does it for us
# Book.objects.all() -> we are not trying to fetch data saved in database, and we can do it by entering class name Book, objects method taken from models.Model 
# and .all() method allowing to see all objects instantiated from class