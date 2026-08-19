from datetime import date, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .models import Book, Member, Issue


def books(request):
    search = request.GET.get("search", "")

    if search:
        books_list = Book.objects.filter(
            title__icontains=search
        ) | Book.objects.filter(
            author__icontains=search
        ) | Book.objects.filter(
            category__icontains=search
        )
    else:
        books_list = Book.objects.all()

    paginator = Paginator(books_list, 5)

    page_number = request.GET.get("page")

    books = paginator.get_page(page_number)
    return render(request, "management/books.html", {
        "books": books,
        "search": search
    })


def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author = request.POST.get("author")
        category = request.POST.get("category")
        isbn = request.POST.get("isbn")
        
        Book.objects.create(
            title=title,
            author=author,
            category=category,
            isbn=isbn
        )
        return redirect("books")
    
    return render(request, "management/add_book.html")


def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.category = request.POST.get("category")
        book.isbn = request.POST.get("isbn")
        book.save()
        return redirect("books")
    
    return render(request, "management/edit_book.html", {"book": book})


def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect("books")


def members(request):
    search = request.GET.get("search", "")

    if search:
        members_list = Member.objects.filter(
            name__icontains=search
        ) | Member.objects.filter(
            email__icontains=search
        )
    else:
        members_list = Member.objects.all()

    paginator = Paginator(members_list, 5)
    page_number = request.GET.get("page")
    members_page = paginator.get_page(page_number)
    
    return render(request, "management/members.html", {
        "members": members_page,
        "search": search
    })


def add_member(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        
        Member.objects.create(
            name=name,
            email=email,
            phone=phone
        )
        return redirect("members")
    
    return render(request, "management/add_member.html")


def edit_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    
    if request.method == "POST":
        member.name = request.POST.get("name")
        member.email = request.POST.get("email")
        member.phone = request.POST.get("phone")
        member.save()
        return redirect("members")
    
    return render(request, "management/edit_member.html", {"member": member})


def delete_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    member.delete()
    return redirect("members")


def issue_book(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        member_id = request.POST.get("member_id")
        
        book = get_object_or_404(Book, pk=book_id)
        member = get_object_or_404(Member, pk=member_id)
        
        Issue.objects.create(
            book=book,
            member=member,
            issue_date=date.today()
        )
        return redirect("issued_books")
    
    books = Book.objects.all()
    members = Member.objects.all()
    
    return render(request, "management/issue_book.html", {
        "books": books,
        "members": members
    })


def issued_books(request):
    issues = Issue.objects.all()
    return render(request, "management/issued_books.html", {"issues": issues})


def return_book(request, pk):
    issue = get_object_or_404(Issue, pk=pk)
    issue.return_date = date.today()
    issue.save()
    return redirect("issued_books")


def home(request):
    total_books = Book.objects.count()
    total_members = Member.objects.count()
    issued_books_count = Issue.objects.filter(return_date__isnull=True).count()
    
    return render(request, "management/home.html", {
        "total_books": total_books,
        "total_members": total_members,
        "issued_books_count": issued_books_count
    })