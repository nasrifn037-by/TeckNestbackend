from django.contrib import admin
from .models import (
    Product,
    category,
    Cart,
    CartItem,
    Oder,
    OderItem,
    Userprofile,
    Review,
)


admin.site.register(Review)
admin.site.register(Product)
admin.site.register(category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Oder)
admin.site.register(OderItem)
admin.site.register(Userprofile)