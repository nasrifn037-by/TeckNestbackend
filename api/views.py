from .models import Userprofile
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, category, Cart, CartItem , Oder, OderItem ,Review
from .serializers import (
    OderSerializer,
    Productserializers,
    categoryserializers,
    Cartserializers,
    RegisterSerializer,
    UserSerializer,
    CartItemserializers,
     ReviewSerializer,
)



@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def profile_update(request):
    print(request.data)

    profile, created = Userprofile.objects.get_or_create(
        user=request.user
    )

    if "photo" in request.FILES:
        profile.photo = request.FILES["photo"]

    profile.phone = request.data.get(
        "phone",
        profile.phone
    )

    profile.address = request.data.get(
        "address",
        profile.address
    )

    profile.save()

    return Response({
        "message": "Profile updated successfully"
    })


@api_view(["GET"])
def get_products(request):
    products = Product.objects.all()

    serializer = Productserializers(
        products,
        many=True,
        context={"request": request}
    )

    return Response(serializer.data)

@api_view(['GET'])
def get_product(request, pk):
    try:
        product = Product.objects.get(id=pk)
        serializer = Productserializers(
            product,
            context={"request": request}
        )
        return Response(serializer.data)

    except Product.DoesNotExist:
        return Response(
            {"error": "Product does not exist"},
            status=404
        )


@api_view(['GET'])
def get_Categories(request):
    categories = category.objects.all()
    serializer = categoryserializers(categories, many=True)
    return Response(serializer.data)


# ---------------- CART ---------------- #

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_Cart(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    serializer = Cartserializers(
        cart,
        context={"request": request}
    )

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_Cart(request):
 

    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity", 1)

    if not product_id:
        return Response({"error": "product_id is required"}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += int(quantity)
    else:
        item.quantity = int(quantity)

    item.save()

    serializer = Cartserializers(
    cart,
    context={"request": request}
    )

    return Response(
    {
        "message": "Product added to cart successfully",
        "cart": serializer.data,
    },
    status=200,
   )



# register api
@api_view(["POST"])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():

        user = serializer.save()

        Userprofile.objects.create(
            user=user
        )

        return Response(
            {"message": "User registered successfully"},
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_orders(request):

    orders = Oder.objects.filter(
        user=request.user
    )

    serializer = OderSerializer(
        orders,
        many=True
    )

    return Response(serializer.data)

# Login API
@api_view(["POST"])
def login(request):
    email = (request.data.get("email") or "").strip()
    password = (request.data.get("password") or "").strip()
    print(request.data)
    if not email or not password:
        return Response(
            {"error": "Email and password are required"},
            status=400
        )

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response(
            {"error": "Invalid Email"},
            status=400
        )

    user = authenticate(
        username=user.username,
        password=password
    )

    if user is None:
        return Response(
            {"error": "Invalid Password"},
            status=400
        )

    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):

    profile, created = Userprofile.objects.get_or_create(
        user=request.user
    )

    return Response({
        "username": request.user.username,
        "email": request.user.email,
        "phone": profile.phone,
        "address": profile.address,
        "photo": request.build_absolute_uri(profile.photo.url)
        if profile.photo else None
    })




@api_view(["POST"])
@permission_classes([IsAuthenticated])
def place_order(request):

    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        return Response({"error": "Cart not found"}, status=404)

    if cart.items.count() == 0:
        return Response({"error": "Your cart is empty"}, status=400)

   

    order = Oder.objects.create(
    user=request.user,
    full_name=request.data["full_name"],
    email=request.data["email"],
    phone=request.data["phone"],
    address=request.data["address"],
    total_amount=cart.total,
    )

    for item in cart.items.all():
        OderItem.objects.create(
            Oder=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )

    cart.items.all().delete()

    serializer = OderSerializer(order)

    return Response(
        {
            "message": "Order Placed Successfully",
            "order": serializer.data,
        },
        status=201,
    )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_cart_quantity(request, item_id):

    try:
        cart = Cart.objects.get(user=request.user)

        item = CartItem.objects.get(
            id=item_id,
            cart=cart
        )

        quantity = request.data.get("quantity")

        item.quantity = quantity
        item.save()

        return Response({
            "message": "Quantity Updated"
        })

    except CartItem.DoesNotExist:
        return Response(
            {"error": "Item Not Found"},
            status=404
        )


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_cart_quantity(request, item_id):

    item = CartItem.objects.get(id=item_id)

    item.quantity = request.data.get("quantity")
    item.save()

    return Response({"message": "updated"})


@api_view(["GET"])
def product_reviews(request, product_id):

    reviews = Review.objects.filter(
        product_id=product_id
    ).order_by("-created_at")

    serializer = ReviewSerializer(
        reviews,
        many=True
    )

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_review(request, product_id):

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(
            {"error": "Product not found"},
            status=404
        )

    serializer = ReviewSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save(
            user=request.user,
            product=product
        )

        print(serializer.errors)

        return Response(
            serializer.data,
            status=201
        )
    
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def Remove_from_Cart(request, item_id):

    try:
        cart = Cart.objects.get(user=request.user)

        item = CartItem.objects.get(
            id=item_id,
            cart=cart
        )

        item.delete()

        return Response({
            "message": "Item Removed Successfully"
        })

    except CartItem.DoesNotExist:
        return Response(
            {
                "error": "Item Not Found"
            },
            status=404
        )





@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def cancel_order(request, order_id):

    try:
        order = Oder.objects.get(
            id=order_id,
            user=request.user
        )

        order.delete()

        return Response({
            "message": "Order Cancelled Successfully"
        })

    except Oder.DoesNotExist:
        return Response(
            {
                "error": "Order Not Found"
            },
            status=404
        )