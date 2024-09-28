from django.db import models


# Create your models here.
class Product(models.Model):
    CHOICES = [
        (1, "⭐"),
        (2, "⭐⭐"),
        (3, "⭐⭐⭐"),
        (4, "⭐⭐⭐⭐"),
        (5, "⭐⭐⭐⭐⭐"),
    ]
    name = models.CharField(max_length=30)
    description = models.TextField()
    old_price = models.DecimalField(decimal_places=2, max_digits=10)
    new_price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    ratings = models.IntegerField(choices=CHOICES, blank=True, null=True)
    is_sale = models.BooleanField(default=False)
    images = models.ImageField(upload_to="posts/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.new_price}"


class Product_Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=Product.CHOICES)
    sold_count = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return (
            f"{self.product.name} - Reyting: {self.rating}, Sotilgan: {self.sold_count}"
        )


class Product_Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body = models.TextField()

    def __str__(self):
        return f" {self.name} --> {self.body[:20]} "
