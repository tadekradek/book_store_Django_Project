from django.contrib import admin

from .models import Book, Author #importing my model

# This is really useful element to customize the admin page of your project. You are able to access the database there, edit and perform a lot of operations that might be of help when it 
# comes to browse and access your data

#
# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    pass


class BookAdmin(admin.ModelAdmin): #creating new class, typically named as class that I am using with "Admin" added, this is to reflect some functionalities in admin page
    # readonly_fields = ("slug",)  #to disable the edition of this attribute in admin site
    prepopulated_fields = {"slug": ("title", )}  # in order to make it working, you need to remove the readonly_fields, or at least remove slug from it, as you would like to see it being edited in real time
    list_filter = ("author","rating",)
    list_display = ("title","author","rating",)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin) #registering my model