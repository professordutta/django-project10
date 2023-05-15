from django.shortcuts import render,HttpResponse,redirect
from .models import Product,Order
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.db import IntegrityError
from django.contrib.auth.models import User
from time import time

# Create your views here.
API_KEY = 'MYKEY'
API_SEC = 'TOPSECRET'

endpoint_secret = 'whsec_8fb08cc6328f47fde48754288193e21ace05740e63724dcbef184ac85bd9681a'
stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = 'http://127.0.0.1:8000'
def home(request):
    my_product=Product.objects.all()
    context={
        "myproduct":my_product
    }
    return render(request,'myntra_app/index.html',context)

def loginuser(request):
    if request.method=='GET':
        form=AuthenticationForm()
        return render(request,'myntra_app/login.html',{'form':form})
    else:
        form=AuthenticationForm()
        uname=request.POST['username']
        upwd=request.POST['password']
        user=authenticate(username=uname,password=upwd)
        if user is not None:
            login(request,user)
            return redirect('mycart')
        else:
            return render(request,'myntra_app/login.html',{'form':form,'message':'invalid password or username'})
  
def logoutuser(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method=='GET':
        return render(request,'myntra_app/register.html')
    else:
        uname=request.POST['email']
        upwd1=request.POST['password1']
        upwd2=request.POST['password2']
        if upwd1==upwd2:
            try:
                user=User.objects.create_user(username=uname,password=upwd1)
                user.save()
                login(request,user)
                return redirect('mycart')
            except IntegrityError:
                return render(request,'myntra_app/register.html',{'message':'Username already exists Choose another one'})
        else:
            return render(request,'myntra_app/register.html',{'message':'Password mismatch error'})
        
def mycart(request):
    return render(request,'myntra_app/mycart.html')

@csrf_exempt
@login_required(login_url='loginuser')
def checkout(request):
 if request.method=="POST":
    data=json.load(request)
    amount=data['post_data']
    order=json.dumps(data['cart'])
    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
    'price_data': {
    'currency': 'inr',
    'product_data': {
    'name': 'Intro to Django Course',
    },
    'unit_amount':amount*100,
    },
    'quantity': 1,
    }],
    metadata={
       'order':order,
       'email':request.user
    },
    mode='payment',
    success_url='http://127.0.0.1:8000/orders/',
    cancel_url=YOUR_DOMAIN + '/cancel',
    )
    return JsonResponse({'id': session.id})
 
# @login_required(login_url='loginuser')  

def orders(request):
    if request.method=="GET":
        o_count=Order.objects.all().filter(email_id=request.user).count()
        if(o_count==0):
            return render(request,"myntra_app/order_history.html",{'message':"No Previous Orders"})
        else:
            
            orders=Order.objects.all().filter(email_id=request.user)       
            return render(request,"myntra_app/order_history.html",{'context':orders})
       
        

@csrf_exempt
def webhook(request):
  mail=request.user
  payload = request.body
  sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)
  
  # Handle the checkout.session.completed event
  if event['type'] == 'checkout.session.completed':
    session = event['data']['object']
    

    # Save an order in your database, marked as 'awaiting payment'
    create_order(session)

    # Check if the order is already paid (for example, from a card payment)
    #
    # A delayed notification payment will have an `unpaid` status, as
    # you're still waiting for funds to be transferred from the customer's
    # account.
    if session.payment_status == "paid":
      data=session['metadata']['order']
      mail=session['metadata']['email']
      # Fulfill the purchase
      fulfill_order(data,mail)

  elif event['type'] == 'checkout.session.async_payment_succeeded':
    session = event['data']['object']

    # Fulfill the purchase
    fulfill_order(session)

  elif event['type'] == 'checkout.session.async_payment_failed':
    session = event['data']['object']

    # Send an email to the customer asking them to retry their order
    return redirect("home")

  # Passed signature verification
  return HttpResponse(status=200)

def fulfill_order(a,mail):
  # TODO: fill me in
  print(a)
  data=json.loads(a)
  o_id=Order.objects.all().count()+1
  id=title=price=count=image=""
  total=0
  for i in range(0,len(data)):
    id+=data[i]['i']+"/"
    title+=data[i]["title"]+"/"
    price+=data[i]['price']+"/"
    image+=data[i]['image_url']+","
    total+=int(data[i]['price'])*data[i]['count']
    count+=str(data[i]['count'])+"/"
  b=Order(Order_id=o_id,
    email_id=mail,
    product_id=id,
    product_title=title,
    product_price=price,
    product_count=count,
    product_image=image,
    total_amount=total)
  b.save()
  print("Fulfilling order")

def create_order(session):
  # TODO: fill me in
  print("Creating order")




