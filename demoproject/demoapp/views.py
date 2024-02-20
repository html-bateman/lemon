

from datetime import datetime
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, APIView, renderer_classes, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from demoapp.throttle import TenCallsPerMinute
from rest_framework.renderers import TemplateHTMLRenderer, StaticHTMLRenderer
from django.shortcuts import render, get_object_or_404
from demoapp.forms import InputForm, BookingForm, UserCommentsForm
from .models import Test, Book, Rating, UserComments
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from rest_framework import generics
from .models import MenuItem, Category, Booking
from .serializers import MenuItemSerializer, BookingSerializer, BookSerializer, MenuItemSerializerHide, CategorySerializer, RatingSerializer

# Create your views here.


def index(request):
    # return HttpResponse("Hello, world. This is the index view of Demoapp.")
    return render(request, 'index.html')


@api_view(['POST', 'GET'])
def test001(request):
    return Response('this is a test', status=status.HTTP_200_OK)


class Test():
    @staticmethod
    @api_view()
    def test002(request):
        return Response({'message': 'list of orders'}, 200)


class BookViewTest(APIView):
    def get(self, request, pk):
        return Response({"message": "single book with id " + str(pk)}, status.HTTP_200_OK)

    def put(self, request, pk):
        return Response({"title": request.data.get('title')}, status.HTTP_200_OK)


class BookViewAuthor(APIView):
    def get(self, request):
        author = request.GET.get('author')
        if (author):
            return Response({'message': 'list of the books by '+author}, status.HTTP_200_OK)
        return Response({'message': 'list of the books'}, status.HTTP_200_OK)

    def post(self, request):
        return Response({'title': request.data.get('title')}, status.HTTP_201_CREATED)


class BookViewT(viewsets.ViewSet):
    def list(self, request):
        return Response({"message": "All books"}, status.HTTP_200_OK)

    def create(self, request):
        return Response({"message": "Creating a book"}, status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        return Response({"message": "Updating a book"}, status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        return Response({"message": "Displaying a book"}, status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        return Response({"message": "Partially updating a book"}, status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        return Response({"message": "Deleting a book"}, status.HTTP_200_OK)


def home(request):
    return render(request, 'home.html', {})


def register(request):
    return render(request, 'register.html', {})


def login(request):
    return render(request, "login.html", {})


def what(request):
    path = request.path
    method = request.method
    content = ''' 
<center><h2>Testing Django Request Response Objects</h2> 
<p>Request path : " {}</p> 
<p>Request Method :{}</p></center> 
'''.format(path, method)
    return HttpResponse(content)


def pathview(request, name, id):
    return HttpResponse("Name:{} UserID:{}".format(name, id))


def qryview(request):
    name = request.GET['name']
    id = request.GET['id']
    return HttpResponse("Name:{} UserID:{}".format(name, id))


def drinks(request, drink_name):
    drink = {
        "mocha": "type of coffe",
        "tea": "type of beverage",
        "lemonlade": "type of refreshment",
        "hamburger": "i miss Mcspicy so much"
    }
    choiceOfDrink = drink[drink_name]
    return HttpResponse(f"<h2>{drink_name}</h2>"+choiceOfDrink)


def about(request):
    content = {
        'about': 'be disciplined',
        'what': 'what is disciipline'
    }
    return render(request, 'about.html', content)


def menu(request):
    return render(request, "menu.html")


def form_view(request):
    form = InputForm()
    context = {"form": form}
    return render(request, "home.html", context)


def usercomment_formview(request):
    form = UserCommentsForm()
    if request.method == 'POST':
        form = UserCommentsForm(request.POST)
        if form.is_valid():
            cleandata = form.cleaned_data
            usercomment = UserComments(
                first_name=cleandata['first_name'],
                last_name=cleandata['last_name'],
                comment=cleandata['comment'],
            )
            usercomment.save()
            return JsonResponse({'message': 'success'})
    return render(request, 'comments.html', {'form': form})


@csrf_exempt
def book(request):
    # return HttpResponse("Make a booking")
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'success'})
    context = {'form': form}
    return render(request, 'book.html', context)


def booking_view(request):
    date = request.GET.get('date', datetime.today().date())
    bookings = Booking.objects.all()
    # booking_json = BookingSerializer('json', bookings)
    return render(request, "bookings.html", {"bookings": bookings})


def test(request):
    # menuItem = {'name':'greek salad'}
    menuItem = {'mains': [
        {'name': 'falafel', 'price': '12'},
        {'name': 'shawarma', 'price': '15'},
    ]}
    return render(request, 'test.html', menuItem)


def test_by_id(request):
    newmenu = Test.objects.all()
    newmenu_dict = {'menu': newmenu}
    return render(request, 'test_by_id.html', newmenu_dict)


@csrf_exempt
def books(request):
    if request.method == 'GET':
        books = Book.objects.all().values()
        return JsonResponse({'books': list(books)})
    elif request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        price = request.POST.get('price')
        book = Book(title=title, author=author, price=price)
        try:
            book.save()
        except IntegrityError:
            return JsonResponse({'error': 'true', 'message': 'required field missing'}, status=400)
        return JsonResponse(model_to_dict(Book), status=201)


class MenuItemView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class MenuItemsViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price', 'inventory']
    # filterset_fields = ['price', 'inventory']
    search_fields = ['title', 'category__title']

    def get_throttles(self):
        if self.action == 'create':
            throttle_classes = [UserRateThrottle]
        else:
            throttle_classes = []
        return [throttle() for throttle in throttle_classes]


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BookView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class SingleBookView(generics.RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class RatingsView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if (self.request.method == 'GET'):
            return []
        return [IsAuthenticated]


# @api_view()
# def menu_items(request):
#     items = MenuItem.objects.all()
#     # items = MenuItem.objects.select_related('category').all()
#     # serialized_item = MenuItemSerializerHide(items, many=True)
#     serialized_item = MenuItemSerializer(
#         items, many=True, context={'request': request})
#     return Response(serialized_item.data)


@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price)
        if search:
            items = items.filter(title__icontains=search)
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)

        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []

        serialized_item = MenuItemSerializerHide(
            items, many=True, context={'request': request})
        return Response(serialized_item.data)
    if request.method == 'POST':
        serialized_item = MenuItemSerializerHide(
            data=request.data, context={'request': request})
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)


@api_view()
def single_item(request, pk):
    # item = MenuItem.objects.get(pk=pk)
    item = get_object_or_404(MenuItem, pk=pk)
    serialized_item = MenuItemSerializerHide(item)
    return Response(serialized_item.data)


@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data)


@api_view()
@renderer_classes([TemplateHTMLRenderer])
def menu(request):
    items = MenuItem.objects.select_related('category').all()
    serialized_item = MenuItemSerializer(items, many=True)
    return Response({'data': serialized_item.data}, template_name='menu-items.html')


@api_view()
@renderer_classes([StaticHTMLRenderer])
def welcome(requst):
    data = '<html><body><h1>Welcome To Little Lemon API Project</h1></body></html>'
    return Response(data)


# @api_view()
# @renderer_classes([CSVRenderer])
# def menu(request):
#     items = MenuItem.objects.select_related('category').all()
#     serialized_item = MenuItemSerializer(items, many=True)
#     return Response({'data': serialized_item.data}, template_name='menu-items.html')

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message": "some secrect message"})


@api_view()
@permission_classes([IsAuthenticated])
def manager(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message": "Only Manager Should See This"})
    else:
        return Response({"message": "You are not authorized"}, 403)


@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message": "successful"})


@api_view()
@permission_classes([IsAuthenticated])
# @throttle_classes([UserRateThrottle])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
    return Response({"message": "message for the looged in user only"})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name='Manager')
        if request.method == 'POST':
            managers.user_set.add(user)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
        return Response({"message": "ok"})
    return Response({"message": "error"}, status.HTTP_400_BAD_REQUEST)
