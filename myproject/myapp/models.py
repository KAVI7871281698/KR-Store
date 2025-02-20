from django.db import models 
from django.core.validators import RegexValidator
# Create your models here.
class signup_page(models.Model):
    fname=models.CharField(max_length=20)
    # lname=models.CharField(max_length=20)
    email=models.EmailField(max_length=50,primary_key=True)
    password=models.CharField(max_length=10)
    address = models.TextField(null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be in the format: '+999999999'. Up to 15 digits allowed."
    )
    mobile = models.CharField(validators=[phone_regex], max_length=15, blank=True, null=True)
    # address = models.TextField(null=True, blank=True)
    # file=models.ImageField(upload_to='uploads/',null=True)
    # confirm_password=models.CharField(max_length=10)


class Feedback(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField(max_length=30)
    feedback=models.CharField(max_length=200)  

class Demart(models.Model):
    brand_name = models.CharField(max_length=30, null=True)
    product_id = models.CharField(max_length=50, unique=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    demart_img = models.ImageField(upload_to='uploads/')

class add_to_cart(models.Model):
    # ForeignKey referencing the demart model
    product = models.ForeignKey(Demart, on_delete=models.CASCADE)  # Foreign key for product_id
    # Other fields in the add_to_cart model
    email = models.CharField(max_length=50, null=True)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    order_date = models.DateTimeField(auto_now_add=True)  # Order date

class Ordernow(models.Model):  # Order Model
    name=models.CharField(max_length=20, null=True)
    email = models.CharField(max_length=50, null=True)
    quantity = models.IntegerField(default=1)
    demart_img = models.ImageField(upload_to='uploads/',null=True)
    product_name = models.CharField(max_length=50,null=True)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    order = models.ForeignKey(add_to_cart, on_delete=models.CASCADE) 
    # quantity = models.ForeignKey(add_to_cart, on_delete=models.CASCADE) 
    order_date = models.DateTimeField(auto_now_add=True) 
    address = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )







