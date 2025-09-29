from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from .forms import CustomUserCreationForm 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model   # removed: login
from reviews.models import Review
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

User = get_user_model()

def signup(request):
    # Redirect already logged-in users
    if request.user.is_authenticated:
        return redirect('profile')

    account_created = False

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Do NOT auto-login
            account_created = True
            # Provide a fresh empty form after success (optional)
            form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/signup.html', {
        'form': form,
        'account_created': account_created,
    })

@login_required
def profile(request):
    me = request.user
    following = me.following.all()
    followers = User.objects.filter(following=me)
    reviews = Review.objects.filter(user=me).select_related("book").order_by("-created")

    return render(request, "users/profile.html", {
        "profile_user": me,
        "following": following,
        "followers": followers,
        "reviews": reviews,
        "is_self": True,
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

@login_required
def public_profile(request, user_id):
    user_profile = get_object_or_404(User, id=user_id)

    following = user_profile.following.all()
    followers = User.objects.filter(following=user_profile)
    reviews = Review.objects.filter(user=user_profile).select_related("book").order_by("-created")

    # Consider self-view routed via /users/profile/, but if someone hits /users/user/<id>/ for themselves:
    is_self = request.user.id == user_profile.id

    return render(request, "users/profile.html", {
        "profile_user": user_profile,
        "following": following,
        "followers": followers,
        "reviews": reviews,
        "is_self": is_self,
    })

@login_required
def unfollow(request, user_id):
    target = get_object_or_404(User, id=user_id)
    if request.method == 'POST' and target != request.user:
        request.user.following.remove(target)
    return redirect('profile')

@login_required
def follow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    # Prevent following self
    if target_user == request.user:
        return HttpResponseForbidden("You cannot follow yourself.")

    if request.method == "POST":
        # Add to following list if not already there
        if not request.user.following.filter(id=target_user.id).exists():
            request.user.following.add(target_user)
        # Redirect back to the public profile page
        return redirect('public_profile', user_id=target_user.id)

    # If someone somehow sends a GET request, just redirect
    return redirect('public_profile', user_id=target_user.id)

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True  # Redirect if already logged in

    def get_success_url(self):
        return reverse_lazy('profile')