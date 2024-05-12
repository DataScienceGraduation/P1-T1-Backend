from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from urbanbackend.models import CustomerUser, Order, Cart, OrderItem, Product
from rest_framework.authtoken.models import Token


@csrf_exempt
@require_POST
def getOrders(request):
    request_data = request.POST
    token = request_data.get('token')
    if not token:
        return JsonResponse({'message': 'Invalid Request'}, status=400)
    token = Token.objects.get(key=token).user
    if not token:
        return JsonResponse({'message': 'Invalid Request'}, status=400)
    orders = Order.objects.filter(user=token)
    dict_orders = []
    for order in orders:
        order_items = []
        for item in order.items.all():
            order_items.append({'product_id': item.product.id, 'quantity': item.quantity, 'total': item.total})
        dict_orders.append({'orderid': order.id, 'orderstatus': order.status, 'ordertotal': order.total,
                            'orderitems': order_items})
    return JsonResponse({'message': 'Orders retrieved', 'orders': dict_orders}, status=200)


@csrf_exempt
@require_GET
def getCart(request):
    request_data = request.POST
    token = request_data.get('token')
    if not token:
        return JsonResponse({'message': 'Invalid Request'}, status=400)
    token = Token.objects.get(key=token).user
    if not token:
        return JsonResponse({'message': 'Invalid Request'}, status=400)
    cart = Cart.objects.get(user=token)
    cart_items = []
    for item in cart.items.all():
        cart_items.append({'product_id': item.product.id, 'quantity': item.quantity})
    return JsonResponse({'message': 'Cart retrieved', 'cart': {'cartid': cart.id, 'cartitems': cart_items}, 'total': cart.total}, status=200)


@csrf_exempt
@require_POST
def deleteCart(request):
    request_data = request.POST
    token = request_data.get('token')
    if not token:
        return JsonResponse({'message': 'Invalid Request'}, status=400)
    token = Token.objects.get(key=token).user
    if not token:
        return JsonResponse({'message': 'Invalid Request'}, status=400)
    cart = Cart.objects.get(user=token)
    cart.delete()
    return JsonResponse({'message': 'Cart deleted'}, status=200)


@csrf_exempt
@require_POST
def addToCart(request):
    request_data = request.POST
    token = request_data.get('token')
    product_id = request_data.get('product_id')
    quantity = request_data.get('quantity')
    if not token or not product_id or not quantity:
        return JsonResponse({'message': 'Invalid Request'}, status=400)
    token = Token.objects.get(key=token).user
    product = Product.objects.get(id=product_id)
    if not token or not product:
        return JsonResponse({'message': 'Invalid Request'}, status=400)
    orderItem = OrderItem.objects.create(product=product, quantity=quantity, total=int(quantity) * product.price)
    cart = Cart.objects.get(user=token)
    if not cart:
        cart = Cart.objects.create(user=token)
    cart.items.add(orderItem)
    return JsonResponse({'message': 'Item added to cart'}, status=200)


@csrf_exempt
@require_POST
def getOrder(request):
    request_data = request.POST
    token = request_data.get('token')
    order_id = request_data.get('orderid')
    if not token or not order_id:
        return JsonResponse({'message': 'Invalid Request'}, status=400)
    token = Token.objects.get(key=token).user
    if not token:
        return JsonResponse({'message': 'Invalid Request'}, status=400)
    # get user order
    order = Order.objects.get(id=order_id)
    orderuser = CustomerUser.objects.get(id=order.user_id)
    if orderuser != token:
        return JsonResponse({'message': 'Invalid Request'}, status=400)
    order_items = []
    for item in order.items.all():
        order_items.append({'product_id': item.product.id, 'quantity': item.quantity, 'total': item.total})
    return JsonResponse({'message': 'Order retrieved', 'order': {'orderid': order.id, 'orderstatus': order.status,
                                                 'ordertotal': order.total, 'orderitems': order_items}}, status=200)


@csrf_exempt
@require_POST
def createOrder(request):
    request_data = request.POST
    token = request_data.get('token')
    if not token:
        return JsonResponse({'message': 'Invalid Request'}, status=400)
    token = Token.objects.get(key=token).user
    if not token:
        return JsonResponse({'message': 'Invalid Request'}, status=400)
    cart = Cart.objects.get(user=token)
    if not cart:
        return JsonResponse({'message': 'Invalid Request'}, status=400)
    order = Order.objects.create(user=token, total=cart.total, status='Pending')
    for item in cart.items.all():
        order.items.add(item)
    cart.delete()
    return JsonResponse({'message': 'Order created'}, status=200)
