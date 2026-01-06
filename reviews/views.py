from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, Review
from .forms import BookForm, ReviewForm
from django.db.models import Q, Count, Avg
from django.urls import reverse


def book_detail(request, book_id):
    """Display a book's details along with its related reviews."""
    book = get_object_or_404(Book, id=book_id)
    reviews = (
        Review.objects.filter(book=book).select_related("user").order_by("-created")
    )

    has_reviewed = False
    if request.user.is_authenticated:
        has_reviewed = Review.objects.filter(book=book, user=request.user).exists()

    context = {
        "book": book,
        "reviews": reviews,
        "can_review": request.user.is_authenticated and not has_reviewed,
        "has_reviewed": has_reviewed,
    }
    return render(request, "reviews/book_detail.html", context)


@login_required
def create_book(request):
    """Create a new book and redirect to its detail page on success."""
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
    """Create a review for the given book and redirect on success."""
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            # Redirect to book detail with anchor to the new review
            url = reverse("book_detail", args=[book.id]) + f"#review-{review.id}"
            return redirect(url)
    else:
        form = ReviewForm()

    reviews = Review.objects.filter(book=book).select_related("user")
    return render(
        request,
        "reviews/create_review.html",
        {"form": form, "book": book, "reviews": reviews},
    )


def home(request):
    """Render the homepage feed for authenticated or anonymous users."""
    show_all = request.GET.get("all") == "1"
    reviews = []

    if request.user.is_authenticated and not show_all:
        # Logged-in personalized feed
        following_users = request.user.following.all()
        reviews = Review.objects.filter(
            Q(user__in=following_users) | Q(user=request.user)
        ).select_related("book", "user")
        is_self = True
    else:
        # Anonymous OR "show all" clicked
        reviews = Review.objects.all().select_related("book", "user")
        is_self = request.user.is_authenticated

    reviews = reviews.order_by("-created")

    return render(
        request,
        "home.html",
        {
            "reviews": reviews,
            "is_self": is_self,
            "show_all": show_all,
        },
    )


def search_books(request):
    """Search books by partial title and render matching results."""
    query = request.GET.get("q", "")
    results = []

    if query:
        results = Book.objects.filter(title__icontains=query).annotate(
            review_count=Count("review", distinct=True),
            avg_rating=Avg("review__rating"),
        )

    return render(
        request, "reviews/search_books.html", {"query": query, "results": results}
    )


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this review.")
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = ReviewForm(instance=review)
    return render(request, "reviews/edit_review.html", {"form": form, "review": review})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this review.")
    if request.method == "POST":
        review.delete()
    return redirect("profile")
