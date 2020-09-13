from django.shortcuts import render, get_object_or_404, redirect
from books.forms import BookForm
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from books.models import Book, AssignedBooks
from accounts.form import NewUserForm


def BookListAsIndex(request):
    try:
        is_librarian = User.objects.filter(librarian__is_librarian=True, username=request.user.username)
        if request.user.is_authenticated and is_librarian:
            book_list = Book.objects.all()
            context = {
                'books': book_list,
                'is_librarian': True if is_librarian else False
            }
            return render(request, 'books/dashboard.html', context)
        elif request.user.is_authenticated and not is_librarian:
            book_list = Book.objects.all()
            context = {
                'books': book_list,
                'is_librarian': True if is_librarian else False
            }
            return render(request, 'books/booklist.html', context)
        else:
            form = NewUserForm(request.POST)
            if form.is_valid():
                form.save()
                form = NewUserForm()
            else:
                print(form.errors)
            context = {
                'form': form
            }
            return render(request, 'accounts/register.html', context)

    except (Book.DoesNotExist, User.DoesNotExist):
        return render(request, 'books/404.html')


@login_required(login_url='/accounts/login/')
def BookDetials(request, id):
    try:
        book = get_object_or_404(Book, pk=id)
        is_librarian = User.objects.filter(librarian__is_librarian=True, username=request.user.username)
        context = {
            'book': book,
            'is_librarian': True if is_librarian else False
        }
        return render(request, 'books/bookdetail.html', context)
    except Book.DoesNotExist:
        return render(request, 'books/404.html')


@login_required(login_url='/accounts/login/')
def IssueBook(request, id):
    try:
        message = ''
        book = get_object_or_404(Book, pk=id)
        user = request.user
        book_assignment, created = AssignedBooks.objects.get_or_create(user=user, book=book)
        book.stock -= 1
        book.save()
        if created:
            message = "Your Request has been sent to Librarian. You will see your book in list as soon as he accepts the requets."
        assigned_booklist = AssignedBooks.objects.filter(user=request.user, issue_request='i')
        context = {
            'books': assigned_booklist,
            'message': message
        }
        return render(request, 'books/issuedbooks.html', context)
    except Book.DoesNotExist:
        return render(request, 'books/404.html')


@login_required(login_url='/accounts/login/')
def ViewIssueRequests(request):
    try:
        requested_booklist = []
        is_librarian = User.objects.filter(librarian__is_librarian=True, username=request.user.username)
        if is_librarian:
            requested_booklist = AssignedBooks.objects.filter(issue_request='r')
            context = {
                'books': requested_booklist,
                'message': 'success'
            }
        else:
            context = {
                'message': 'failure'
            }

        return render(request, 'books/requestedbooks.html', context)
    except Book.DoesNotExist:
        return render(request, 'books/404.html')


@login_required(login_url='/accounts/login/')
def AddBooks(request):
    try:
        is_librarian = User.objects.filter(librarian__is_librarian=True, username=request.user.username)
        if request.user.is_authenticated and is_librarian:
            form = BookForm(request.POST, request.FILES or None)
            if form.is_valid():
                product = form.save(commit=False)
                product.added_by = request.user
                product.save()
                return redirect('/')
            context = {
                'form': form
            }
            return render(request, 'books/addbook.html', context)
        else:
            return HttpResponse('<center> Only Admin Have rights to add the products </center>')
    except Book.DoesNotExist:
        return render(request, 'books/404.html')


@login_required(login_url='/accounts/login/')
def AcceptIssueRequests(request, id):
    try:
        is_librarian = User.objects.filter(librarian__is_librarian=True, username=request.user.username)
        if request.user.is_authenticated and is_librarian:
            requested_book = AssignedBooks.objects.filter(issue_request='r',id=id).first()
            if requested_book:
                requested_book.issue_request = 'i'
                requested_book.save()
            book_list = Book.objects.all()
            context = {
                'books': book_list,
                'is_librarian': True if is_librarian else False
            }
        return render(request, 'books/dashboard.html',context)
    except Book.DoesNotExist:
        return render(request, 'books/404.html')
