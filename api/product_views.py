from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from urbanbackend.models import CustomerUser
from rest_framework.authtoken.models import Token
from urbanbackend.models import Product, Category


@csrf_exempt
@require_GET
def getFeaturedProducts(request):
    feature_product_list = Product.objects.filter(is_featured=True)
    return JsonResponse({'products': list(feature_product_list.values())}, status=200)

@csrf_exempt
@require_POST
def getAllProducts(request):
    request_data = request.POST
    category = request_data.get('category')
    if category is None or category == 'all':
        product_list = Product.objects.all()
        return JsonResponse({'products': list(product_list.values())}, status=200)

    filtered_products = Product.objects.filter(category=category.name)
    return JsonResponse({'products': list(filtered_products.values())}, status=200)

@csrf_exempt
@require_GET
def getProduct(request):
    request_data = request.POST
    name = request_data.get('name')
    product = Product.objects.get(name=name)
    product_detail = {'product': product}
    return JsonResponse(product_detail, status=200)

@csrf_exempt
@require_GET
def getCategories(request):
    Category_list = Category.objects.all()
    return JsonResponse({'Categories': list(Category_list.values())}, status=200)
