from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),

    # Books
    path("books/", views.books, name="books"),
    path("books/add/", views.add_book, name="add_book"),
    path("books/edit/<int:id>/", views.edit_book, name="edit_book"),
    path("books/delete/<int:id>/", views.delete_book, name="delete_book"),

    # Members
    path("members/", views.members, name="members"),
    path("members/add/", views.add_member, name="add_member"),
    path("members/edit/<int:id>/", views.edit_member, name="edit_member"),
    path("members/delete/<int:id>/", views.delete_member, name="delete_member"),

    # Issue / Return
    path("issued-books/", views.issued_books, name="issued_books"),
    path("issue-book/", views.issue_book, name="issue_book"),
    path("return-book/<int:id>/", views.return_book, name="return_book"),
]