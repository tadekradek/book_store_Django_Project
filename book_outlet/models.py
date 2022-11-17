from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify #module to transform text (title) into slugfield

# Create your models here. #every time I edit models.py file, I need to make sure that I make migration to sent instruction for Django how to update database


class Country(models.Model):
    name = models.CharField(max_length=80)
    code = models.CharField(max_length=2)
    
    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Countries"


class Address(models.Model):
    street = models.CharField(max_length=80)
    postal_code = models.CharField(max_length=5)
    city = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.street}, {self.postal_code}, {self.city}"

    class Meta:  # nested class in class is standard, but advanced and not often used python syntax
        verbose_name_plural = "Address Entries" #this is useful feature for amending the way how name is output
    
class Author(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    address = models.OneToOneField(Address, on_delete=models.CASCADE,null=True) #models.OneToOneField is a classs dedicated to one to one relations

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model): #my class that I just created inherits from Django-specific models.Model class that is useful and provides built-in functionalites
    title = models.CharField(default = "", max_length = 50)
    rating = models.IntegerField(default = 1)  # from a dedicated django library core.validators, some useful feature to customize elements
                                                                                              # selected from database based on some validator, e.g max, min
    #author = models.CharField(default = "", null = True, max_length = 100) #now I allowed to fill blanks with null value, alternative is blank = True to allow empty fields in database - not allowed by default                                              
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True) #now definining attribute by pointing to another class, on_delete parameter decides what should happen with related models if one of those gets deleted,
                                                                 # CASCADE says that if author gets deleted, all books by these author are deleted in cascaded way, 
                                                                 # alternative to try PROTECT, SET_NULL
                                                                 # ForeignKey class is dedicated to one-to-many connections
    is_bestselling = models.BooleanField(default = False)
    slug = models.SlugField(default = "", blank=True,
                            null=False,  db_index=True)   # Django-specific slug value type, enusre that whatever is stored inside, will be in format harry-potter-1,
                                                                       # adding db_index would make searching a bit more efficient, however, you should not add index to every column, as the operation as it is decreases the performance
                                                                       # choose wisely, attach index to the column you are using the most for queries
    published_countries = models.ManyToManyField(Country,related_name="books") #thats how you set up many-to-many relation, you cannot add on_delete property here, because many-to-many, because there are more t
                                                          # than only two relations as for one-to-many and one-to-one, and we dont want to store the list 
                                                          # for many-to-many relations, there is no direct assignment available like author.published_countries = germany, because
                                                          # due to many to many nature of relation, it is not single value but its a list of values, so we are using 
                                                          #author.published_countries.add()

    def get_absolute_url(self):
        return reverse("book-detail-slug", args=[self.slug]) # very useful to create url creation logic once and utilize anywhere in the code

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs) #apart from overwriting save method, we need to ensure that the built-in django save method is also executed

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

# in order to provide more detailed information related to database, like number of all books, sum of ratings etc, there are aggregation methods in django
#

# books_by_rowling = Book.objects.filter(author__last_name="Rowling") filtering by data being in relationship is very intuitive, very powerful method to query across relations
# we can also access by adverse relation
# >>> jkr.book_set -> we are accessing the inverse relation