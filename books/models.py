from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from datetime import datetime, timedelta


class Book(models.Model):
    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    name = models.CharField(_("Book"), max_length=50)
    author = models.CharField(_("Author"), max_length=50)
    price = models.PositiveIntegerField(_("Price"))
    stock = models.PositiveIntegerField(_("Stock"))
    image = models.ImageField(_("Cover"), upload_to='images/')

    def __str__(self):
        return "[BOOK] {}".format(self.name)


class Librarian(models.Model):
    class Meta:
        verbose_name = 'Librarian'

    librarian = models.ForeignKey(User, verbose_name=_("Librarian"), on_delete=models.CASCADE,
                                  related_name="librarian")
    is_librarian = models.BooleanField(_("is_librarian"), default=True)

    def __str__(self):
        return "[LIBRARIAN] {}".format(self.librarian)


class AssignedBooks(models.Model):
    ASSIGNMENT_TYPE = (
        ("i", "Issued"),
        ("r", "Requested"),
    )

    class Meta:
        verbose_name = 'Book Assignment'
        verbose_name_plural = 'Book Assignments'

    user = models.ForeignKey(User, verbose_name=_("Issuer"), on_delete=models.CASCADE,
                             related_name="issuer")
    book = models.ForeignKey(Book, verbose_name=_("Issued Book"), on_delete=models.CASCADE,
                             related_name="issued_book")
    issue_request = models.CharField(_("Book Assignments Status"), max_length=1,
                                     choices=ASSIGNMENT_TYPE, default='r')
    issue_date = models.DateTimeField(default=datetime.now)
    renewal_date = models.DateTimeField(default=datetime.now() + timedelta(days=30))

    def __str__(self):
        return "[BOOK] {} [USER] {}".format(self.book,self.user)
