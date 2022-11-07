from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator

# Create your models here. #every time I edit models.py file, I need to make sure that I make migration to sent instruction for Django how to update database

class Book(models.Model): #my class that I just created inherits from Django-specific models.Model class that is useful and provides built-in functionalites
    title = models.CharField(max_length = 50)
    rating = models.IntegerField(validators = [MinLengthValidator(1), MaxValueValidator(5)])  # from a dedicated django library core.validators, some useful feature to customize elements
                                                                                              # selected from database based on some validator, e.g max, min
    author = models.CharField(null = True, max_length = 100) #now I allowed to fill blanks with null value, alternative is blank = True to allow empty fields in database - not allowed by default                                              
    is_bestselling = models.BooleanField(default = False)

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