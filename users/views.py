from django.shortcuts import get_object_or_404, render, redirect
from .forms import CustomUserCreationForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, get_user_model
from reviews.models import Review
from django.db.models import Q

User = get_user_model()

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required
def profile(request):
    user_profile = request.user
    # Fetch reviews by this logged-in user
    reviews = Review.objects.filter(user=user_profile).select_related("book")
    return render(request, "users/profile.html", {
        "profile_user": user_profile,
        "reviews": reviews
    })

@login_required
def search_users(request):
    query = request.GET.get("q", "")
    results = []
    if query:
        results = User.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id)  # exclude current user
    return render(request, "users/search_users.html", {
        "query": query,
        "results": results
    })

def public_profile(request, user_id):
    user_profile = get_object_or_404(User, id=user_id)
    reviews = Review.objects.filter(user=user_profile).select_related("book")
    return render(request, "users/public_profile.html", {
        "profile_user": user_profile,
        "reviews": reviews
    })