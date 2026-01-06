from django import forms
from .models import Book, Review


class BookForm(forms.ModelForm):
    """Form for creating or editing book records."""

    class Meta:
        model = Book
        fields = ["title", "description", "image"]


class ReviewForm(forms.ModelForm):
    """Form for creating or editing reviews without book/user fields."""

    class Meta:
        model = Review
        fields = ["headline", "body", "rating"]
