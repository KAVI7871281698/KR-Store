from django.conf import settings
from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .models import signup_page,Feedback,Demart,add_to_cart,Ordernow
from django.contrib import messages
from functools import wraps
from django.db.models import Q
import os
import datetime
from django.db.models import Sum 
from django.core.mail import EmailMessage
# import razorpay
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
   
# Create your views here.
def login_required(f):
    @wraps(f) 
    def wrapped(request,*args,**kwargs):
        if not request.session.get('is_logged_in'):
            return redirect('signin')
        return f(request,*args,**kwargs)
    return wrapped
        

def signup(request):
    if request.method=='POST':
        fname=request.POST['fname']
        email=request.POST['email']
        address=request.POST['address']
        mobile = request.POST['mobile']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']

        if password!=confirm_password:
            messages.error(request,'Password does not match')
            return redirect('signup')

        if signup_page.objects.filter(email=email).exists():
            messages.error(request,'Email already exits')
            return redirect('signin')
        database_save=signup_page(fname=fname,email=email,password=password,address=address,mobile=mobile)
        database_save.save()
        messages.success(request,'Regiester Successfully')
        return redirect('signin')
    
    return render(request, 'signup.html')

def signin(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']

        try:
            take_data=signup_page.objects.get(email=email)
            if take_data.password==password:
                request.session['email']=email
                request.session['fname']=take_data.fname
                request.session['is_logged_in']=True
                return redirect('index')
            else:
                messages.error(request,'Incorrect Password')
        except:
            messages.error(request,'Incorrect Email')

    return render(request,'signin.html')

@login_required
def index(request):
    return render(request,'index.html')

def admin(request):
    return render(request,'adminlogin.html')

@login_required
def demarts(request):
    show=Demart.objects.filter(category='Ready to cook')
    return render(request, 'demart.html', {'see':show})

@login_required
def demartstationary(request):
    show = Demart.objects.filter(category='stationary')
    return render(request,'demartstationary.html',{'see':show})

@login_required
def skincares(request):
    show=Demart.objects.filter(category='skincare')
    return render(request,'demart.html',{'see':show})

@login_required
def about(request):
    return render(request,'about.html')

@login_required
def cleaner(request):
    show=Demart.objects.filter(category='cleaner')
    return render(request,'cleaner.html',{'see':show})

@login_required
def chocolates(request):
    show=Demart.objects.filter(category='chocolate')
    return render(request,'chocolates.html',{'see':show})

@login_required
def electricals(request):
    show=Demart.objects.filter(brand_name='spencers',category='electrical')
    return render(request,'electricals.html',{'see':show})

@login_required
def kitchen(request):
    show=Demart.objects.filter(brand_name='spencers',category='kitchen')
    return render(request,'kitchen.html',{'see':show})

@login_required
def spencers(request):
    show=Demart.objects.filter(brand_name='spencers',category='personal care')
    return render(request,'spencers.html',{'see':show})

@login_required
def loggout(request):
    request.session.flush()
    return redirect('signin')

@login_required
def product(request):
    show=Demart.objects.filter(brand_name='fruits',category='fruits')
    return render(request,'product.html',{'see':show})

@login_required
def vegtables(request):
    show=Demart.objects.filter(brand_name='vegatables',category='vegtables')
    return render(request,'vegtables.html',{'see':show})

@login_required
def grocery(request):
    show=Demart.objects.filter(brand_name='grocery',category='grocery')
    return render(request,'grocery.html',{'see':show})

@login_required
def carts(request, id):
    sample = get_object_or_404(Demart, id=id)  
    email = request.session.get('email')  
    # Save product to the cart
    saved = add_to_cart(product=sample, email=email)
    saved.save()

    # Check for multiple possible redirect pages
    possible_pages = ['spencers', 'product', 'demarts', 'demartstationary', 'skincares']
    
    for page in possible_pages:
        if request.GET.get(page):  # If any of these is found in the GET parameters
            return redirect(request.GET.get(page))

    # Fallback to previous page or default page
    return redirect(request.META.get('HTTP_REFERER', '/product'))  

@login_required
def add(request):
    email=request.session.get('email')
    show = add_to_cart.objects.filter(email=email)
    return render(request,'add_to_cart.html',{'carts':show})

@login_required
def delete(request,id):
    delete_items = add_to_cart.objects.get(id=id)
    delete_items.delete()
    return redirect('add_to_cart')

@login_required
def order_now(request,id, ids):
    order_details = Demart.objects.get(id=id)
    order_details2 = add_to_cart.objects.get(id=ids)
    quantity = order_details2.quantity
    total_price = order_details2.total_price
    email = request.session.get('email')
    see = add_to_cart.objects.filter(email=email).last()
    return render(request,'order_now.html',{'ordered':order_details2})

@login_required
def increase_quantity(request, id):
    item = get_object_or_404(add_to_cart, id=id)
    item.quantity += 1 

    # Update total price only if quantity > 1, otherwise set to product price
    item.total_price = item.quantity * item.product.price if item.quantity > 1 else item.product.price
    
    item.save()
    return redirect('add_to_cart')

@login_required
def decrease_quantity(request, id):
    item = get_object_or_404(add_to_cart, id=id)
    
    if item.quantity > 1:
        item.quantity -= 1  
        item.total_price = item.quantity * item.product.price
        item.save()
    else:
        # If quantity is 1, set total_price to just product price
        item.total_price = item.product.price
        item.save()

    return redirect('add_to_cart')

@login_required
def order_confirm(request,id):
    if request.method == 'POST':
        user_address = request.POST['address']
        confirm_order = add_to_cart.objects.get(id=id)
        user_img = confirm_order.product.demart_img
        user_product_name = confirm_order.product.product_name
        user_product_price = confirm_order.product.price
        user_total_price = confirm_order.total_price
        user_quantity = confirm_order.quantity
        user_email = request.session.get('email')
        user_name = request.session.get('fname')
        store = Ordernow(order=confirm_order,address=user_address,name=user_name,product_price=user_product_price,email=user_email,quantity=user_quantity,product_name=user_product_name,total_price=user_total_price,demart_img=user_img)
        store.save()
        
                # Prepare email
        subject = "Order Confirmation - Your Order has been Placed!"
        body = f"""
        Hello {user_name},

        Your order has been successfully placed! Here are the details:

        📦 Product: {user_product_name}
        💰 Price: ${user_product_price}
        🔢 Quantity: {user_quantity}
        💵 Total Price: ${user_total_price}
        📍 Shipping Address: {user_address}
         img:{user_img}

        Thank you for shopping with us!

        Best Regards,  
        Your Company
        """
        # user_emails = "kavi7871281698@gmail.com"

        email = EmailMessage(
            subject,
            body,
            'krstorer84@gmail.com',  # Developer Gmail
            [user_email]  # Customer's email
        )
        # Attach image if it exists

        if user_img:
            image_path = os.path.join(settings.MEDIA_ROOT, str(user_img))  # Get the full image path
            if os.path.exists(image_path):
                with open(image_path, 'rb') as img:
                    email.attach(user_img.name, img.read(), 'image/jpeg')  # Adjust MIME type if needed

        email.send()  # Send the email

        return render(request,'order_confirm.html')
    
    user_email = request.session.get('email')
    view = add_to_cart.objects.filter(email=user_email).last()
    return render(request,'order_confirm.html',{'show':view})

STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Processing', 'Processing'), #give the status value are tuple method
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
]

@login_required
def order_list(request):
    orders = Ordernow.objects.all()  # Get all orders
    return render(request, 'order_list.html', {'orders': orders, 'status_choices': STATUS_CHOICES})

@login_required
def update_order_status(request, id):
    order = get_object_or_404(Ordernow, id=id)
    
    # Only allow admin to update the status
    if request.user.is_superuser:
        if request.method == "POST":
            new_status = request.POST.get('status')
            if new_status in dict(STATUS_CHOICES):
                order.status = new_status
                order.save()
    
    return redirect('order_list')  # Redirect to the order list

@login_required
def cancel_order(request, id):
    order = get_object_or_404(Ordernow, id=id)

    if request.user.is_authenticated and request.session.get('email') == order.email:
        if order.status != 'Delivered':
            order.status = 'Cancelled'
            order.save()
    
    return redirect('order_list')

@login_required
def shipped(request):
    user_email = request.session.get('email')
    orders = Ordernow.objects.filter(email=user_email)  # Get all orders
    return render(request, 'shipped.html', {'orders': orders})

@login_required
def dashboard(request):
    recent_order = Ordernow.objects.all().order_by('-id')[:3]
    total_sales = Ordernow.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0   # Number Sales 
    total_orders = Ordernow.objects.count() #Number of Product on sale
    return render(request,'dashboard.html',{'recent_order':recent_order,'total_sales':total_sales,'total_orders':total_orders})

@login_required
def dashboard_customer(request):
    customer = signup_page.objects.all()
    return render(request,'dashboard_customer.html',{'see':customer})

@login_required
def dashboard_product(request):
    product = Demart.objects.all()
    return render(request,'dashboard_product.html',{'product_items':product})

@login_required
def dashboard_order(request):
    orders = Ordernow.objects.all()
    return render(request,'dashboard_order.html',{'order_item':orders})

@login_required
def report(request):
    # Get the current day and month and year
    current_month = datetime.datetime.now().strftime('%B')
    current_year = datetime.datetime.now().year 
    selected_date = request.GET.get('date', datetime.date.today().isoformat())  # Gets 'YYYY-MM-DD' as a string
    selected_date = datetime.date.fromisoformat(selected_date)
    

    # Filter orders for the current month and current year
    monthly_orders = Ordernow.objects.filter(order_month=current_month, order_year=current_year)

    # Calculate total amount for the current month
    total_amount = monthly_orders.aggregate(total_amount =Sum('total_price'))['total_amount'] or 0

    # Calculate the number of order sales on that month
    total_orders = monthly_orders.count()

    #Fliter the order date and day
    daily_orders = Ordernow.objects.filter(order_date=selected_date)

    #Calculate the total amount in particular day
    daily_total_sales = daily_orders.aggregate(total =Sum('total_price'))['total'] or 0

    #Calculate the number of Orders in particular day
    daily_total_orders = daily_orders.count()
    
    return render(request, 'report.html', {
        'report_data': monthly_orders,
        'total_sales': total_amount,
        'month': current_month,
        'year': current_year,
        'orders': total_orders,
        'selected_date': selected_date,
        'daily_amount':  daily_total_sales,
        'daily_orders':  daily_total_orders
    })

@login_required
def feedback(request):
    view = Feedback.objects.all()
    return render(request,'dashboard_feedback.html',{'datas':view})

@login_required
def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        feedback = request.POST['feedback']
        saved = Feedback(name=name,email=email,feedback=feedback)
        saved.save()
    return render(request,'contact.html')
