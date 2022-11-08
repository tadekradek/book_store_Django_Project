from django.shortcuts import render,get_object_or_404
from django.http import Http404

from book_outlet.models import Book

def index(request):
    books = Book.objects.all() # here, why accessing and calling database, you are about to use exactly the same commands as in the shell earlier
    return render(request, "book_outlet/index.html",{"books":books})

def book_detail(request, id):
    # try:
    #     book = Book.objects.get(id = id) # pk is a special key (primary key), that you can always use when you would like to adress the key set up as primary
    # except:
    #     raise Http404()
    book = get_object_or_404(Book, pk=id)
    return render(request, "book_outlet/book_detail.html",{
        "title": book.title,
        "author": book.author,
        "rating": book.rating,
        "is_bestseller":book.is_bestselling
        })
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