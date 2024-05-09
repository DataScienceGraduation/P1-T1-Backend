from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from urbanbackend.models import CustomerUser, Order
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
def addImageToProduct(request):
    from urbanbackend.models import Product
    request_data = request.POST
    product_id = request_data.get('product_id')
    image = request.FILES['image']
    product = Product.objects.get(id=product_id)
    product.image = image
    product.save()
    return JsonResponse({'message': 'Image added to product'}, status=200)


@csrf_exempt
@require_POST
def createOrder(request):
    from urbanbackend.models import OrderItem, Product
    request_data = request.POST
    token = request_data.get('token')
    if not token:
        return JsonResponse({'message': 'Invalid Request'}, status=400)
    token = Token.objects.get(key=token).user
    if not token:
        return JsonResponse({'message': 'Invalid Request'}, status=400)
    items = request_data.get('items')
    total = request_data.get('total')
    status = request_data.get('status')
    order = Order.objects.create(user=token, total=total, status=status)
    # convert items to list of dictionaries
    items = eval(items or '[]')
    for item in items:
        product = Product.objects.get(id=item['product_id'])
        order_item = OrderItem.objects.create(product=product, quantity=item['quantity'],
                                              total=int(item['quantity']) * product.price)
        order.items.add(order_item)
    return JsonResponse({'message': 'Order created'}, status=201)