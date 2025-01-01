import stripe
from django.conf import settings
from django.db import models

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products_images', blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f'Продукт:{self.name} | Категория:{self.category}'

    def save(self, *args, **kwargs):
        if not self.stripe_price_id:
            price = self.create_stripe_price()
            self.stripe_price_id = price.id
        super(Product, self).save(*args, **kwargs)

    def create_stripe_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_price = stripe.Price.create(
            product=stripe_product.id,
            unit_amount=round(self.price*100),
            currency='kzt')
        return stripe_price


class BasketQuerySet(models.QuerySet):
    def total_price(self):
        return sum(basket.sum() for basket in self)

    def total_count(self):
        return sum(basket.quantity for basket in self)

    def stripe_products(self):
        line_items = []
        for basket in self:
            line_items.append(
                {
                    'price': basket.product.stripe_price_id,
                    'quantity': basket.quantity
                }
            )
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Basket: {self.user.email} | Product: {self.product.name} | Quantity: {self.quantity}'

    def sum(self):
        return self.product.price*self.quantity

    def de_json(self):
        return {
            'product_name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'sum': float(self.sum()),
        }
