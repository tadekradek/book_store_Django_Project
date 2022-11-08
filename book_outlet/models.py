from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator
from django.urls import reverse

# Create your models here. #every time I edit models.py file, I need to make sure that I make migration to sent instruction for Django how to update database

class Book(models.Model): #my class that I just created inherits from Django-specific models.Model class that is useful and provides built-in functionalites
    title = models.CharField(max_length = 50)
    rating = models.IntegerField(validators = [MinLengthValidator(1), MaxValueValidator(5)])  # from a dedicated django library core.validators, some useful feature to customize elements
                                                                                              # selected from database based on some validator, e.g max, min
    author = models.CharField(null = True, max_length = 100) #now I allowed to fill blanks with null value, alternative is blank = True to allow empty fields in database - not allowed by default                                              
    is_bestselling = models.BooleanField(default = False)

    def get_absolute_url(self):
        return reverse("book-detail", args=[self.id]) # very useful to create url creation logic once and utilize anywhere in the code

    def __str__(self):
        return f"{self.title} ({self.rating})"   # adding only a method does not require to make a migration, as it is only needed when atributes are changed


# once I tried to do python manage.py makemigrations command, django detected that class now has new attributes, and for instances in databases that I updated earlier there is no
# respective entry for this new attributes, so it aasked me how I am about to tackle that
"""
It is impossible to add a non-nullable field 'author' to book without specifying a default. This is because the database needs something to populate existing rows.
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit and manually define a default value in models.py.
Select an option:
"""


# in the shell, you can access the specific field of the object simply with . notation like this:
#>>> Book.objects.all()[1].author 
#>>> Book.objects.all()[1].title  

# remember, just by adding:
#>>> harry_potter.author = "J.K. Rowling"
#>>> harry_potter.bestselling = True
#nothing happened yet, as any update/change was only done in memory so far, not in database, you need to enter harry_potter.save()
# Django is smart, if you call .save() on already exisiting object, it will not create new one, but update the previous one

# Deleting data
#>>> harry_potter.delete()  -> simple as that 
#(1, {'book_outlet.Book': 1})  -> response from Django how many objects were deleted 
# however, it is not allowed to use .delete() to erase a single attribute, you just need to do it by updating

# Book.objects.create() -> basically the same as Book(title="...").save() but just skips the save at the end

# Book.objects.get(id=3) -> in the argument you can specify that selection criteria, REMEMBER - get will always return only ONE data entry, if multiple objects would be found, it will return error
# Book.objects.filter() -> unlike .get() is able to return more than one object
# Book.objects.filter(rating<3) -> would return error, as the parameter is invalid syntax in python, however
# Book.objects.filter(rating__lt=3) -> Django enables special way to customize the condition  - Field lookups - to check official docs
# Book.objects.filter(rating__lt=3, title__contains="Story") -> to remember, __contains is not case sensitive
# from django.db.models import Q -> special class from django that allows to write queries containing or condition
# Book.objects.filter(Q(rating__lt=3)|Q(is_bestselling=True))  using pipe to define OR condition and also Q() as query in constructor
# Book.objects.filter(Q(rating__lt=3)|Q(is_bestselling=True), Q(author="Stephen King")) OR and AND combination

#Performance
# it is possible to chain filter methods, as simply running Book.objects.filter() returns an object, which is query, and its is possible to do the same once again with different criteria
# also, performance for accessing database is important
# notation
# bestsellers = Book.objects.filter(is_bestselling = True) is not yet producing result from database, but bestsellers is now saved as query to run
# amazing_bestsellers = bestsellers.filter(rating__gt=4)
#>>> amazing_bestsellers
#<QuerySet []> database was not touched yet, which is good for performance
# django runs the query after print(bestsellers)
# it is important, from performance perspective, to hit the database as low number of times as possible

# Entry.objects.filter(pub_date__year=2005).delete() works when you want to delete instances that you selected with the filter condition
#