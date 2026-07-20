from rest_framework import serializers
from .models import Product, category, Cart, CartItem, Oder, OderItem , Review
from django.contrib.auth.models import User
from rest_framework import serializers
class Productserializers(serializers.ModelSerializer):

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_image(self, obj):
        request = self.context.get("request")

        if obj.image:
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url

        return None

class categoryserializers(serializers.ModelSerializer):

    class Meta:
        model = category
        fields = "__all__"



# 2cart

class CartItemserializers(serializers.ModelSerializer):

    name = serializers.CharField(
        source="product.name",
        read_only=True
    )

    price = serializers.DecimalField(
        source="product.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    image = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "quantity",
            "name",
            "price",
            "image",
        ]

    def get_image(self, obj):

        request = self.context.get("request")

        if obj.product.image:

            if request:
                return request.build_absolute_uri(
                    obj.product.image.url
                )

            return obj.product.image.url

        return None

class Cartserializers(serializers.ModelSerializer):

    items = CartItemserializers(
        many=True,
        read_only=True
    )

    total = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "created_at",
            "items",
            "total",
        ]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
    

from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]



class OderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OderItem
        fields = "__all__"


class OderSerializer(serializers.ModelSerializer):

   Item = OderItemSerializer(many=True, read_only=True)

   class Meta:
        model = Oder
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "username",
            "rating",
            "comment",
            "created_at",
            "product",
        ]

        read_only_fields = [
            "id",
            "username",
            "created_at",
            "product",   # 👈 ye line add karo
        ]