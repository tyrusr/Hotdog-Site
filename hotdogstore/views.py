from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, MenuItem, Cart, Purchase, Special
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
import json
from django.http import JsonResponse
import bleach

# Create your views here.

def index(request):

    #gets current special object for home page promotional
    current_special = Special.objects.filter().first()
    return render(request, 'hotdogstore/index.html', {
        "special":current_special
    })

def checkout(request):

    #gets the objects fomr the cart and then adds to purchases and removes from cart
    if request.method == 'POST':
        try:
            user = request.user
            cart_objects = Cart.objects.filter(customer=user)
            for item in cart_objects:
                menu_object = MenuItem.objects.get(item_name=item.item.item_name)
                purchase_object = Purchase.objects.create(purchaser=user, item_purchased=menu_object)
                item.delete()
            return JsonResponse({'success': True, 'redirect_url': reverse('index')})
        
        except Exception as err:
            return render(request, 'hotdogstore/cart.html')

def cart(request):

    #gets all the items in the cart for display purposes
    try:
        user = request.user
        cart_items = Cart.objects.filter(customer=user)
            
        return render(request, 'hotdogstore/cart.html', {
            "cart":cart_items,
        })
        
    except Exception as err:
        return render(request, 'hotdogstore/cart.html')
    

def remove_item(request):
    if request.method == "POST":
        try:
            #recieves data from fetch
            data = json.loads(request.body)
            menu_item = data.get('item')

            #gets the menu item the user selected to remove
            MenuItem_object = MenuItem.objects.get(item_name=menu_item)
            user = request.user

            #removes selected item from cart
            cart_object = Cart.objects.filter(customer=user, item=MenuItem_object).first()
            cart_object.delete()

            return JsonResponse({"success": True, "message": f"Received {menu_item}"})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON"}, status=400)



def update_cart(request):
    if request.method == "POST":
        try:
            #recieves json data from fetch
            data = json.loads(request.body)
            menu_item = data.get('item')

            #finds the menu item object
            MenuItem_object = MenuItem.objects.get(item_name=menu_item)
            user = request.user

            #creates cart object based on user and menu object reference
            cart_object = Cart.objects.create(customer=user, item=MenuItem_object)

            print("Received item:", menu_item, user)

            return JsonResponse({"success": True, "message": f"Received {menu_item}"})
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON"}, status=400)
        

def menu(request):
    
    #gets all menu items from database to pass to html as menu variable
    menu_items = MenuItem.objects.all()
    print(menu_items)
    return render(request, 'hotdogstore/menu.html',{
        "menu":menu_items
    })

def login_user(request):
    if request.method == "POST":
        #gets user credentials from login form
        username = bleach.clean(request.POST.get('username'))
        password = request.POST.get('password')

        #authenticates user
        user = authenticate(username=username, password=password)

        #logs user in if everything correct
        if user is not None:
            login(request, user)
            return redirect('index')
        #returns an error if anything was incorrect
        else:
            return render(request, 'hotdogstore/login.html', {
                "message":"Invalid Username or Password"
            })
    else:
        return render(request, 'hotdogstore/login.html')   
    
def logout_user(request):
    
    #logs out user if they are signed in and redirects them if they arent and somehow get to this url
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    else:
        return render(request, 'hotdogstore/index.html')
    
def register(request):
    if request.method == "POST":

        #get everything from the form
        username = bleach.clean(request.POST.get('username'))
        email = bleach.clean(request.POST.get('email'), tags=[], strip=True)
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        #makes sure username input isnt blank
        check_for_blank = username.strip(" ")
        if check_for_blank == "":
            return render(request, 'hotdogstore/register.html',{
                "message":"Invalid Username"
            })


        #checks if the username already exists
        user_in_database = User.objects.filter(username = username)
        if user_in_database.exists():
            return render(request, 'hotdogstore/register.html',{
                "message":"username already taken"
            })
        
        #checks if email is in valid format        
        try:
            validate_email(email)

        except ValidationError:
            return render(request, 'hotdogstore/register.html',{
                "message":"Invalid Email"
            })
        
        #checks if email already exists
        email_in_database = User.objects.filter(email = email)
        if email_in_database.exists():
            return render(request, 'hotdogstore/register.html',{
                "message":"Email Already Exists"
            })

        #checks if passwords do not match
        if password1 != password2:
            return render(request, 'hotdogstore/register.html',{
                "message":"Passwords Do Not Match"
            })

        #if no problems then create the new user then logs in
        user_object = User.objects.create_user(username=username, email=email, password=password1)

        user = authenticate(username=username, password=password1)

        login(request, user)

        return render(request, 'hotdogstore/index.html')
    else:
        return render(request, 'hotdogstore/register.html')