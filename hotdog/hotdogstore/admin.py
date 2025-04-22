from django.contrib import admin
from .models import MenuItem, Category, Purchase, Cart, Special

# Register your models here.
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Purchase)
admin.site.register(Cart)
admin.site.register(Special)
 