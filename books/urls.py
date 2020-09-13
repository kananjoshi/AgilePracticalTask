from django.urls import path
from books.views import BookDetials, IssueBook, ViewIssueRequests, AddBooks, AcceptIssueRequests

urlpatterns = [
    path(r'detail/<int:id>/', BookDetials, name='bookdetail'),
    path(r'issue/<int:id>/', IssueBook, name='bookissue'),
    path(r'view_issue_request/', ViewIssueRequests, name='view_issue_requests'),
    path(r'addbook/', AddBooks, name='addbook'),
    path(r'accept_issue_req/<int:id>/', AcceptIssueRequests, name='accept_issue_req'),

]
