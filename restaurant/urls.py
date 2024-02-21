from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('reserve/', views.reserve, name='reserve'),
    path('reservations/', views.reservations, name='reservations'),
    path('bookings/', views.bookings, name='bookings'),
    # Add the remaining URL path configurations here
    path('menu/', views.menu, name="menu"),
    path('menu-item/<int:pk>', views.display_menu_item, name="menu_item"),
    path('users/', views.UserView.as_view()),
    path('users/<int:pk>', views.SingleUserView.as_view(), name='user'),
    path('api-menu/', views.MenuView.as_view(), name='api-menu'),
    path('api-menu/<int:pk>', views.SingleMenuView.as_view())
]
