from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt

from storage.custom_storage import AzureBlobStorage
from fuzzywuzzy import process
from urbanbackend.models import Product, Category


azStorage = AzureBlobStorage()


@csrf_exempt
@require_POST
def getFeaturedProducts(request):
    limit = request.POST.get('limit')
    feature_product_list = list(Product.objects.filter(is_featured=True).values())
    if limit is not None:
        feature_product_list = feature_product_list[:min(int(limit), len(feature_product_list))]
    return JsonResponse({'products': feature_product_list}, status=200)


@csrf_exempt
@require_POST
def getProducts(request):
    request_data = request.POST
    category = request_data.get('category')
    if category is None:
        product_list = Product.objects.all()
        products = list(product_list.values())
        return JsonResponse({'products': products}, status=200)

    filtered_products = Product.objects.filter(category=category)
    return JsonResponse({'products': list(filtered_products.values())}, status=200)


@csrf_exempt
@require_POST
def getProduct(request):
    try:
        request_data = request.POST
        id = request_data.get('id')
        if id is None:
            return JsonResponse({'message': 'product id is required'}, status=400)
        if not Product.objects.filter(id=id).exists():
            return JsonResponse({'message': 'product not found'}, status=404)
        product = list(Product.objects.filter(id=id).values())[0]
        return JsonResponse({'product': product}, status=200)
    except Product.DoesNotExist:
        return JsonResponse({'message': 'product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': 'an unknown error occurred'}, status=500)


@csrf_exempt
@require_GET
def getCategories(request):
    Category_list = Category.objects.all()
    return JsonResponse({'Categories': list(Category_list.values())}, status=200)


@csrf_exempt
@require_GET
def Search(request):
    query = request.GET.get('q')
    typoitem = process.extract(query, Product.objects.values_list('name', flat=True), limit=4)
    items = []
    for item in typoitem:
        print(item[0])
        items.append(list(Product.objects.filter(name__icontains=item[0]).values()))
    if not items:
        return JsonResponse({'message': 'product not found'}, status=200)
    return JsonResponse({'Products': items}, status=200)


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
    product.image = azStorage.url(product.image)
    product.save()
    return JsonResponse({'message': 'Image added to product'}, status=200)
