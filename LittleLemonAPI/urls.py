from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.SingeItemView.as_view()),
    path('groups/manager/users', views.manager_view),
    path('groups/manager/users/<int:pk>', views.single_manager_view),
    path('groups/delivery-crew/users', views.deliverycrew_view),
    path('groups/delivery-crew/users/<int:pk>', views.single_deliverycrew_view),
    path('cart/menu-items', views.cart_view),
    path('orders', views.order_view),
    path('orders/<int:pk>', views.single_order_view),
    path('capstone-menu-items/', views.CapstoneMenuItemView.as_view()),
    path('capstone-menu-items/<int:pk>',
         views.CapstoneSingleMenuItemView.as_view()),
    path('api-token-auth/', obtain_auth_token),
]
