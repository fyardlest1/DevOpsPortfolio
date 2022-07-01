from django.core.validators import MinValueValidator
from django.db import models


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    product_in_collection = models.IntegerField(validators=[MinValueValidator(0)])
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)

    # Returning the Collection title
    def __str__(self) -> str:
        return self.title

    # Sorting the data
    class Meta:
        ordering = ['title']

# The store models here.


class Product(models.Model):
    title = models.CharField(max_length=255)  # varchar(255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    # max_digits & decimal_places are always requires (ex: 9999.99)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)])
    inventory = models.IntegerField(validators=[MinValueValidator(0)])
    last_update = models.DateField(auto_now=True)
    # Implement a 1-to-many relationship between Collection & Product
    # A collection can have multiple products
    # on_delete=models.PROTECT means if we are accidently delete a collection we do not delete all the products in that collection
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')
    # Implement a many-to-many relationship between Promotion & Product
    promotions = models.ManyToManyField(Promotion, blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Customer(models.Model):
    # Creating list of Choices -> G for Gold; S for Silver; B for Bronze
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['first_name', 'last_name', 'membership']


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAIL = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAIL, 'Fail'),
    ]
    placed_at = models.DateField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    # Implement a 1-to-many relationship between Customer & Order
    # A customer can have multiple orders
    # if we are accidently delete a customer we do not delete orders
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    # Implement a 1-to-many relationship between Order & Item
    # An Order can have multiple Items
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


# Implement a 1-to-many relationship between Cart & Item
class ShoppingCart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class ShoppingCartItem(models.Model):
    # if we are delete a cart we should delete the items automatically
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


# Implement a 1-to-many relationship between Customer & Address
# Note that a customer should exist before creating an address
# with this Implementation a customer can have more than one address
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=25, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
