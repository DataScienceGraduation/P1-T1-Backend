from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from urbanbackend.models import CustomerUser, Order, Cart, OrderItem, Product
from rest_framework.authtoken.models import Token
from . import messages


@csrf_exempt
@require_POST
def getOrders(request):
    try:
        request_data = request.POST
        token = request_data.get('token')
        if not token:
            return JsonResponse({'message': messages.INVALID_REQUEST}, status=400)
        token = Token.objects.get(key=token).user
        if not token:
            return JsonResponse({'message': messages.INVALID_REQUEST}, status=400)
        orders = Order.objects.filter(user=token)
        dict_orders = []
        for order in orders:
            order_items = []
            for item in order.items.all():
                order_items.append({'product_id': item.product.id, 'quantity': item.quantity, 'total': item.total})
            dict_orders.append({'orderid': order.id, 'orderstatus': order.status, 'ordertotal': order.total,
                                'orderitems': order_items})
        return JsonResponse({'orders': dict_orders}, status=200)
    except:
        return JsonResponse({'message': messages.UNKNOWN_ERROR}, status=500)


@csrf_exempt
@require_GET
def getCart(request):
    try:
        request_data = request.POST
        token = request_data.get('token')
        if not token:
            return JsonResponse({'message': messages.INVALID_REQUEST}, status=400)
        token = Token.objects.get(key=token).user
        if not token:
            return JsonResponse({'message': messages.INVALID_REQUEST}, status=400)
        cart = Cart.objects.get(user=token)
        cart_items = []
        for item in cart.items.all():
            cart_items.append({'product_id': item.product.id, 'quantity': item.quantity})
        return JsonResponse({'cart': {'cartid': cart.id, 'cartitems': cart_items}, 'total': cart.total}, status=200)
    except:
        return JsonResponse({'message': messages.UNKNOWN_ERROR}, status=500)


@csrf_exempt
@require_POST
def deleteCart(request):
    try:
        request_data = request.POST
        token = request_data.get('token')
        if not token:
            return JsonResponse({'message': messages.INVALID_REQUEST}, status=400)
        token = Token.objects.get(key=token).user
        if not token:
            return JsonResponse({'message': messages.INVALID_REQUEST}, status=400)
        if not Cart.objects.filter(user=token).exists():
            return JsonResponse({'message': messages.INVALID_REQUEST}, status=400)
        cart = Cart.objects.get(user=token)
        cart.delete()
        return JsonResponse({'message': messages.CART_DELETED}, status=200)
    except:
        return JsonResponse({'message': messages.UNKNOWN_ERROR}, status=500)


@csrf_exempt
@require_POST
def addToCart(request):
    try:
        request_data = request.POST
        token = request_data.get('token')
        product_id = request_data.get('product_id')
        quantity = request_data.get('quantity')
        if not token or not product_id or not quantity:
            return JsonResponse({'message': messages.INVALID_REQUEST}, status=400)
        token = Token.objects.get(key=token).user
        product = Product.objects.get(id=product_id)
        if not token or not product:
            return JsonResponse({'message': messages.INVALID_REQUEST}, status=400)
        orderItem = OrderItem.objects.create(product=product, quantity=quantity, total=int(quantity) * product.price)
        if not Cart.objects.filter(user=token).exists():
            return JsonResponse({'message': messages.INVALID_REQUEST}, status=400)
        cart = Cart.objects.get(user=token)
        if not cart:
            cart = Cart.objects.create(user=token)
        cart.items.add(orderItem)
        return JsonResponse({'message': messages.ITEM_ADDED_TO_CART}, status=200)
    except:
        return JsonResponse({'message': messages.UNKNOWN_ERROR}, status=500)


@csrf_exempt
@require_POST
def getOrder(request):
    try:
        request_data = request.POST
        token = request_data.get('token')
        order_id = request_data.get('orderid')
        if not token or not order_id:
            return JsonResponse({'message': messages.INVALID_REQUEST}, status=400)
        if not Token.objects.filter(key=token).exists():
            return JsonResponse({'message': messages.INVALID_REQUEST}, status=400)
        token = Token.objects.get(key=token).user
        if not Order.objects.filter(id=order_id).exists():
            return JsonResponse({'message': messages.ORDER_NOT_FOUND}, status=404)
        order = Order.objects.get(id=order_id)
        orderuser = CustomerUser.objects.get(id=order.user_id)
        if orderuser != token:
            return JsonResponse({'message': 'Invalid Request'}, status=400)
        order_items = []
        for item in order.items.all():
            order_items.append({'product_id': item.product.id, 'quantity': item.quantity, 'total': item.total})
        return JsonResponse({'order': {'orderid': order.id, 'orderstatus': order.status,
                                                     'ordertotal': order.total, 'orderitems': order_items}}, status=200)
    except:
        return JsonResponse({'message': messages.UNKNOWN_ERROR}, status=500)


@csrf_exempt
@require_POST
def createOrder(request):
    try:
        request_data = request.POST
        token = request_data.get('token')
        if not token:
            return JsonResponse({'message': messages.INVALID_REQUEST}, status=400)
        token = Token.objects.get(key=token).user
        if not token:
            return JsonResponse({'message': messages.INVALID_REQUEST}, status=400)
        if not Cart.objects.filter(user=token).exists():
            return JsonResponse({'message': messages.INVALID_REQUEST}, status=400)
        cart = Cart.objects.get(user=token)
        order = Order.objects.create(user=token, total=cart.total, status='Pending')
        for item in cart.items.all():
            order.items.add(item)
        cart.delete()
        return JsonResponse({'message': messages.ORDER_CREATED}, status=200)
    except:
        return JsonResponse({'message': messages.UNKNOWN_ERROR}, status=500)
