from django.contrib import admin

from books.models import Book,AssignedBooks,Librarian


class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'stock', 'price', 'author']
    list_search = ['name']

admin.site.register(Book, BookAdmin)

class LibrarianAdmin(admin.ModelAdmin):
    list_display = ['librarian']
    list_search = ['librarian']

admin.site.register(Librarian, LibrarianAdmin)

class AssignedBooksAdmin(admin.ModelAdmin):
    list_display = ['user','book','issue_date','renewal_date','issue_request']
    list_search = ['book','user']

admin.site.register(AssignedBooks, AssignedBooksAdmin)