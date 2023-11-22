"""ChicoGuessr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

from game import views as game_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', game_views.home, name = 'home'),
    path('game/', game_views.game),
    path('join/', game_views.join),
    path('login/', game_views.user_login),
    path('logout/', game_views.user_logout),
    path('userstats/', game_views.user_stats),
    path('aboutus/', game_views.about_us),
    path('server_info/',game_views.server_info),
    path('userstats/<int:userid>/', game_views.search_user_stats),
    path('street/', game_views.loadStreetAPI, name='street'),
    path('map/', game_views.loadMapAPI, name='map'),
]
