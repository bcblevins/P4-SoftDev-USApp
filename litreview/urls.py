"""litreview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from reviews import views as review_views
from django.conf import settings
from django.conf.urls.static import static


# Temporary home view so LOGIN_REDIRECT_URL works
def home(request):
    """Return a simple logged-in welcome message."""
    return HttpResponse("<h1>Welcome, you are logged in!</h1>")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", review_views.home, name="home"),  # home page at root
    path("users/", include("users.urls")),  # add URL patterns from users app
    path("reviews/", include("reviews.urls")),  # add URL patterns from reviews app
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
