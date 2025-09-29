from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .forms import BookForm, ReviewForm
from .models import Book, Review

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = Review.objects.filter(book=book).select_related("user")  # optimize queries
    return render(request, "reviews/book_detail.html", {
        "book": book,
        "reviews": reviews,
    })


@login_required
def create_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            return redirect("book_detail", book_id=book.id)
    else:
        form = BookForm()

    return render(request, "reviews/create_book.html", {"form": form})


@login_required
def create_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book             
            review.user = request.user      
            review.save()
            return redirect("book_detail", book_id=book.id)
    else:
        form = ReviewForm()

    reviews = Review.objects.filter(book=book).select_related("user")
    return render(request, "reviews/create_review.html", {
        "form": form,
        "book": book,
        "reviews": reviews
    })


def home(request):
    if request.user.is_authenticated:
        # Logged-in: get reviews from followed users
        following_users = request.user.following.all()
        reviews = Review.objects.filter(user__in=following_users).select_related("book", "user")
    else:
        # Anonymous: show all reviews (or public subset)
        reviews = Review.objects.all().select_related("book", "user")

    # Sort latest first
    reviews = reviews.order_by('-created')

    return render(request, "home.html", {"reviews": reviews})


def search_books(request):
    query = request.GET.get("q", "")
    results = []
    if query:
        results = Book.objects.filter(title__icontains=query)
    return render(request, "reviews/search_books.html", {
        "query": query,
        "results": results
    })
