from .serializers import OrderItemSerializer, OrderSerializer, OrderStatusSerializer
from .models import Order, OrderItem, CapstoneMenuItem
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from .models import MenuItem, Cart, Order, OrderItem
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, api_view, throttle_classes
from rest_framework.exceptions import PermissionDenied
from .serializers import CapstoneMenuItemSerializer, MenuItemSerializer, UserSerializer, CartSerializer, OrderSerializer, OrderItemSerializer, OrderStatusSerializer


# Create your views here.
class IsManager(permissions.BasePermission):
    message = 'Not authorized!'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.groups.filter(name='Manager').exists():
            return True
        raise PermissionDenied(self.message)


class CapstoneMenuItemView(generics.ListCreateAPIView):
    queryset = CapstoneMenuItem.objects.all()
    serializer_class = CapstoneMenuItemSerializer


class CapstoneSingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CapstoneMenuItem.objects.all()
    serializer_class = CapstoneMenuItemSerializer


class MenuItemView(generics.ListCreateAPIView):
    # queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsManager]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_queryset(self):
        items = MenuItem.objects.select_related('category').all()
        category_name = self.request.query_params.get('category')
        to_price = self.request.query_params.get('to_price')
        search = self.request.query_params.get('search')
        ordering = self.request.query_params.get('ordering')
        perpage = self.request.query_params.get('perpage', default=8)
        page = self.request.query_params.get('page', default=1)

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

        return items


class SingeItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsManager]


@api_view(['POST', 'DELETE', 'GET'])
@permission_classes([IsManager])
def manager_view(request):
    if request.method == 'GET':
        items = User.objects.filter(groups__name='Manager')
        serialized = UserSerializer(items, many=True)
        return Response(serialized.data, status.HTTP_200_OK)

    else:
        user = request.data.get('username')
        try:
            user = User.objects.get(username=user)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        group = Group.objects.get(name='Manager')

        if request.method == 'POST':
            user.groups.add(group)
            return Response({'message': 'User assigned to the manager group'}, status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            user.groups.remove(group)
            return Response({'message': 'User removed to the manager group'}, status.HTTP_200_OK)


@api_view(['GET', 'DELETE'])
@permission_classes([IsManager])
def single_manager_view(request, pk):
    users_in_group = User.objects.filter(groups__name='Manager')
    try:
        item = users_in_group[pk-1]
    except IndexError:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serialized = UserSerializer(item)
        return Response(serialized.data)
    if request.method == 'DELETE':
        group = Group.objects.get(name='Manager')
        item.groups.remove(group)
        return Response({'message': 'User removed to the manager group'}, status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsManager])
def deliverycrew_view(request):
    if request.method == 'GET':
        items = User.objects.filter(groups__name='Delivery crew')
        serialized = UserSerializer(items, many=True)
        return Response(serialized.data, status.HTTP_200_OK)
    elif request.method == 'POST':
        user = request.data.get('username')
        try:
            user = User.objects.get(username=user)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        group = Group.objects.get(name='Delivery crew')
        user.groups.add(group)
        return Response({'message': 'User assigned to the delivery crew'}, status.HTTP_201_CREATED)


@api_view(['GET', 'DELETE'])
@permission_classes([IsManager])
def single_deliverycrew_view(request, pk):
    try:
        item = User.objects.filter(groups__name='Delivery crew')[pk-1]
    except IndexError:
        return Response({"error": "no user found"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serialized = UserSerializer(item)
        return Response(serialized.data)
    if request.method == 'DELETE':
        group = Group.objects.get(name='Delivery crew')
        item.groups.remove(group)
        return Response({'message': 'User removed to the manager group'}, status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
def cart_view(request):
    if (request.method == "GET"):
        items = Cart.objects.filter(user_id=request.user.id)
        serialized = CartSerializer(items, many=True)
        return Response(serialized.data, status.HTTP_200_OK)
    if (request.method == 'POST'):
        serialized_item = CartSerializer(data=request.data)
        serialized_item.is_valid()
        serialized_item.save()
        return Response(serialized_item.data, status=status.HTTP_201_CREATED)
    if (request.method == 'DELETE'):
        queryset = items = Cart.objects.filter(user_id=request.user.id)
        queryset.delete()
        return Response(status.HTTP_200_OK)


@api_view(['POST', 'GET'])
@throttle_classes([UserRateThrottle])
def order_view(request):
    if (request.method == "GET"):
        is_manager = request.user.groups.filter(name='Manager').exists()
        is_delivery = request.user.groups.filter(name='Delivery crew').exists()
        if is_manager:
            items = Order.objects.all()
        elif is_delivery:
            items = Order.objects.filter(delivery_crew_id=request.user.id)
        else:
            items = Order.objects.filter(user_id=request.user.id)

        orderstatus = request.query_params.get('status')
        to_total = request.query_params.get('to_total')
        to_date = request.query_params.get('to_date')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=8)
        page = request.query_params.get('page', default=1)
        if orderstatus:
            items = items.filter(status__exact=orderstatus)
        if to_total:
            items = items.filter(total__lte=to_total)
        if to_date:
            items = items.filter(date__lte=to_date)
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)

        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []

        serialized = OrderSerializer(items, many=True)
        return Response(serialized.data, status.HTTP_200_OK)
    if (request.method == 'POST'):
        if request.data['user'] != request.user.id:
            return Response({'error': 'You can only update your own order.'}, status.HTTP_403_FORBIDDEN)
        serialized_item = OrderSerializer(data=request.data)
        serialized_item.is_valid()
        serialized_item.save()
        cart_items = Cart.objects.filter(user_id=request.user.id)
        if not cart_items:
            return Response({'message': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        order_items = []
        for cart_item in cart_items:
            order_item = OrderItem(
                order=serialized_item.instance,
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price
            )
            order_items.append(order_item)
        OrderItem.objects.bulk_create(order_items)

        cart_items.delete()
        return Response({'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
def single_order_view(request, pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response({'error': 'Order Not Exist'}, status=status.HTTP_404_NOT_FOUND)
    is_manager = request.user.groups.filter(name='Manager').exists()
    is_delivery = request.user.groups.filter(name='Delivery crew').exists()
    if order.user_id != request.user.id and not is_manager and not is_delivery:
        return Response({'error': 'this order does not belong to you'}, status.HTTP_400_BAD_REQUEST)

    if (request.method == 'GET'):
        order_items = OrderItem.objects.filter(order_id=pk)
        serialized = OrderItemSerializer(order_items, many=True)
        return Response(serialized.data, status.HTTP_200_OK)

    if (request.method in ['PATCH', 'PUT']):
        if is_delivery:
            for key in request.data:
                if key != 'status':
                    return Response({'error': 'only order status is allowed to update'}, status.HTTP_403_FORBIDDEN)

            serialized_item = OrderStatusSerializer(
                order, data=request.data, context={'request': request})
        elif is_manager:
            serialized_item = OrderSerializer(order, data=request.data)
        else:
            return Response({'error': 'User not authorized'}, status.HTTP_401_UNAUTHORIZED)

        if serialized_item.is_valid():
            serialized_item.save()
            return Response({'message': 'order updated'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serialized_item.errors, status=status.HTTP_400_BAD_REQUEST)

    if (request.method == 'DELETE'):
        if is_manager:
            order.delete()
            return Response("order deleted", status=status.HTTP_202_ACCEPTED)
        else:
            return Response("no permission", status.HTTP_403_FORBIDDEN)
