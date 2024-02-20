from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path('index/', views.index, name='index'),
    path('', views.home),
    path('what/', views.what),
    path('getuser/<name>/<id>', views.pathview, name='pathview'),
    path('getuser/', views.qryview, name='qryview'),
    path("menu/", views.menu),
    path('drink/<str:drink_name>/', views.drinks, name="drink_name"),
    path("about/", views.about),
    path("book/", views.book, name='book'),
    path("home/", views.form_view),
    path("test/", views.test),
    path("test_by_id", views.test_by_id),
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    # path('api/books/', views.books),
    path('test001', views.test001),
    path('test002/', views.Test.test002),
    path('test/<int:pk>', views.BookViewTest.as_view()),
    path('test4', views.BookViewAuthor.as_view()),
    path('test003', views.BookViewT.as_view(
        {
            'get': 'list',
            'post': 'create',
        })
    ),
    path('tests/<int:pk>', views.BookViewT.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        })
    ),
    # path('menu-items', views.MenuItemView.as_view()),
    # path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('menu-items', views.MenuItemsViewSet.as_view({'get': 'list'})),
    path('menu-items/<int:pk>',
         views.MenuItemsViewSet.as_view({'get': 'retrieve', 'post': 'create'})),
    # path('menu-items', views.menu_items),
    # path('menu-items/<int:pk>', views.single_item),
    path('menu', views.menu),
    path('welcome', views.welcome),
    path('booking/', views.booking_view, name='booking'),
    path('books', views.BookView.as_view()),
    path('books/<int:pk>', views.SingleBookView.as_view()),
    path('category', views.CategoriesView.as_view()),
    path('category/<int:pk>', views.category_detail, name='category-detail'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('secret/', views.secret),
    path('api-token-auth', obtain_auth_token),
    path('manager/', views.manager),
    path('throttle-check', views.throttle_check),
    path('throttle-check-auth', views.throttle_check_auth),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/blacklist/', TokenBlacklistView.as_view(),
    #      name='token_blacklist'),
    path('groups/manager/users', views.managers),
    path('ratings', views.RatingsView.as_view()),
    path('comments', views.usercomment_formview),
]

# router = SimpleRouter(trailing_slash=False)
# router.register('tests', views.BookViewT, basename='tests')
# urlpatterns = router.urls

# router = DefaultRouter(trailing_slash=False)
# router.register('tests', views.BookViewT, basename='tests')
# urlpatterns = router.urls
