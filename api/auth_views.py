from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from urbanbackend.models import CustomerUser
from rest_framework.authtoken.models import Token
from . import messages

@csrf_exempt
@require_POST
def signup(request):
    try:
        request_data = request.POST
        username = request_data.get('username')
        name = request_data.get('name')
        password = request_data.get('password')
        email = request_data.get('email')
        phone = request_data.get('phone')
        apartment = request_data.get('apartment')
        address = request_data.get('street')
        governorate = request_data.get('governorate')
        zipcode = request_data.get('zipcode')
        if not username or not name or not password or not email or not phone or not apartment or not address or not governorate or not zipcode:
            return JsonResponse({'message': 'Missing required fields'}, status=400)
        if CustomerUser.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Username already exists'}, status=400)
        if CustomerUser.objects.filter(email=email).exists():
            return JsonResponse({'message': 'Email already exists'}, status=400)
        if CustomerUser.objects.filter(phone=phone).exists():
            return JsonResponse({'message': 'Phone number already exists'}, status=400)
        if validate_password(password) is not None:
            return JsonResponse({'message': 'Password is not strong enough'}, status=400)
        user = CustomerUser.objects.create_user(username=username, password=password, email=email)
        user.name = name
        user.phone = phone
        user.apartmentNo = apartment
        user.address = address
        user.governorate = governorate
        user.zipcode = zipcode
        user.save()
        return JsonResponse({'message': 'User created'}, status=201)
    except:
        return JsonResponse({'message': messages.UNKNOWN_ERROR}, status=500)


@csrf_exempt
@require_POST
def signin(request):
    try:
        request_data = request.POST
        name = request_data.get('name')
        password = request_data.get('password')
        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            return JsonResponse({'token': token.key}, status=200, safe=False)
        return JsonResponse({'message': 'Invalid Name or Password, Please Try Again'}, status=400)
    except:
        return JsonResponse({'message': messages.UNKNOWN_ERROR}, status=500)


@csrf_exempt
@require_POST
def logout(request):
    try:
        request_data = request.POST
        token = request_data.get('token')
        if token:
            token = Token.objects.get(key=token)
            user = token.user
            Token.objects.filter(user=user).delete()
            return JsonResponse({'message': 'User logged out'}, status=200)
    except:
        return JsonResponse({'message': messages.UNKNOWN_ERROR}, status=500)


@csrf_exempt
@require_POST
def isAuth(request):
    try:
        request_data = request.POST
        token = request_data.get('token')
        if Token.objects.filter(key=token).exists():
            return JsonResponse({'message': messages.USER_NOT_AUTHENTICATED}, status=400)
        return JsonResponse({'message': messages.USER_AUTHENTICATED}, status=200)
    except:
        return JsonResponse({'message': messages.UNKNOWN_ERROR}, status=500)

@csrf_exempt
@require_POST
def whoami(request):
    try:
        request_data = request.POST
        token = request_data.get('token')
        if not Token.objects.filter(key=token).exists():
            return JsonResponse({'message': messages.USER_NOT_AUTHENTICATED}, status=200)
        user = Token.objects.get(key=token).user
        return JsonResponse(
            {'username': user.username, 'email': user.email, 'phone': user.phone, 'apartment': user.apartmentNo,
             'street': user.address, 'governorate': user.governorate, 'zipcode': user.zipcode}, status=200)
    except:
        return JsonResponse({'message': messages.UNKNOWN_ERROR}, status=500)
