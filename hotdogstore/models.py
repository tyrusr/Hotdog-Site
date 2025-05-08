from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    
class MenuItem(models.Model):
    item_name = models.CharField(max_length=255)
    item_price = models.DecimalField(max_digits=4, decimal_places=2)
    item_image = models.CharField(max_length=255)
    item_description = models.CharField(max_length=500)
    item_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.item_name

class Purchase(models.Model):
    purchaser = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    item_purchased = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

    def __str__(self):
        return f"User:{self.purchaser}  Item Purchased:{self.item_purchased}"
    
class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

    def __str__(self):
        return f"Customer: {self.customer}  Item: {self.item}"

class Special(models.Model):
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)

    def __str__(self):
        return f"Item: {self.item}"
