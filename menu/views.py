from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from decimal import Decimal
from .models import PizzaType, Size, NumOfTopping, Topping, Meal, Salad, Pasta, \
    AddExtra, NumExtraOption, SubType, Sub, SubExtraOption, DinnerPlatter, PizzaOrder, Cart


# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return render(request, "menu/index.html", {"message": None})
    context = {
        "user": request.user,
        "pizza_types": PizzaType.objects.all(),
        "sizes": Size.objects.all(),
        "num_of_topping": NumOfTopping.objects.all(),
        "all_toppings": Topping.objects.all(),
        "pizza_order": PizzaOrder.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "meal_option": Meal.objects.all(),
        "salad_w_tuna": list(Meal.objects.all())[6],
        "sub_type": SubType.objects.all(),
        "sub": Sub.objects.all(),
        "sub_extra_option": SubExtraOption.objects.all(),
        "num_extra_option": NumExtraOption.objects.all(),
        "add_extra": AddExtra.objects.all(),
        "numbers": range(6)
    }

    return render(request, "menu/menu.html", context)


# The next 5 routes/urls relate to authenticating the user
def access_register(request):
    return render(request, "menu/register.html", {"message": None})


def register(request):
    username = request.POST["username"]
    password = request.POST["password"]
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    user = User.objects.create_user(username, email, password)
    user.first_name = first_name
    user.last_name = last_name

    user.save()
    return HttpResponseRedirect(reverse("access_login"))


def access_login(request):
    return render(request, "menu/login.html", {"message": None})


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        request.session["user"] = username
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "menu/login.html", {"message": "Invalid Credentials. Please login again or Register"})


def logout_view(request):
    logout(request)
    return render(request, "menu/login.html", {"message": "Logged out."})


def total_order(request):
    pizza_order = ""
    toppings = ""
    pasta_order = ""
    salad_order = ""
    dinner_platter_order = ""
    sub_sandwich_order = ""
    selections = ""
    show_extra = ""
    total = 0

    # -----------------------------------------pizza
    try:
        type_of_pizza = request.POST["pizza_type"]
        size = request.POST["pizza_size"]
        if request.POST.getlist("topping_choice") is not None:
            toppings = request.POST.getlist("topping_choice")
            topping_num = len(toppings)
        else:
            topping_num = 0
        pizza_order = PizzaOrder.objects.get(pizza_order_type__pizzatype=type_of_pizza,
                                             pizza_order_size__size=size,
                                             pizza_num_of_topping__num_of_topping=topping_num)
        total += pizza_order.price


    except:
        pass

    # ---------------------------------------pasta
    try:
        pasta_option = request.POST["a_pasta"]
        pasta_order = Pasta.objects.get(type=pasta_option)
        total += pasta_order.price

    except:

        pass
    # --------------------------------------salad
    try:
        salad_option = request.POST["a_salad"]
        salad_order = Salad.objects.get(salad_meal__meal_type=salad_option)
        total += salad_order.price

    except:
        pass

    # ----------------------------------------dinnerplatter
    try:
        dinner_option = request.POST["a_dinner"]
        dinner_size = request.POST["dinner_size"]
        dinner_platter_order = DinnerPlatter.objects.get(dinner_meal__meal_type=dinner_option,
                                                         dinner_platter_size__size=dinner_size)
        total += dinner_platter_order.price

    except:
        pass
    # ----------------------------------------sub
    try:

        sandwich = request.POST["sandwich"]
        sub_size = request.POST["sandwich_size"]
        sub_sandwich_order = Sub.objects.get(sub_type__sub_type=sandwich, size__size=sub_size)
        total += sub_sandwich_order.price
        try:
            if request.POST["extra_cheese"] is not None:
                extra_cheese = request.POST["extra_cheese"]
                extra_c_price = Decimal(extra_cheese)
                show_extra = AddExtra.objects.first()
                total += extra_c_price
        except:
            pass
        try:
            if request.POST.getlist("sub_extra") is not None:
                selections = request.POST.getlist("sub_extra")
                sel_price = Decimal(len(selections) * .5)
                print(sel_price, selections)
                total += sel_price
        except:
            pass
    except:
        pass

#This context is solely for displaying the users selected choices to the user
    context = {
        "pizza_order": pizza_order,
        "toppings": toppings,
        "pasta_order": pasta_order,
        "salad_order": salad_order,
        "dinner_platter_order": dinner_platter_order,
        "sub_order": sub_sandwich_order,
        "extra": show_extra,
        "selections": selections,
        "total": total
    }

    # This section stores the selections in a "cart" for retrieval. Cart items are updated or newly created as required
    entire_cart = str(pizza_order) + str(toppings) + str(pasta_order) + str(salad_order) + str(dinner_platter_order) + \
                  str(sub_sandwich_order)
    print(request.session["user"], entire_cart, total)
    Cart.objects.update_or_create(username__username=request.session["user"],
                                  defaults={"order_entire": entire_cart,
                                            "total_price": total,
                                            "order_pizza": str(pizza_order),
                                            "order_pizza_topping": str(toppings),
                                            "order_pasta": str(pasta_order),
                                            "order_salad": str(salad_order),
                                            "order_sub": str(sub_sandwich_order),
                                            "order_extra": str(show_extra),
                                            "order_selections": str(selections),
                                            "order_dinner_platter": str(dinner_platter_order),
                                            "username": User.objects.get(username=request.session["user"])})
    return render(request, "menu/cart.html", context)


def cart(request):
    # This page is for retrieving the cart details(items placed in shopping cart) from the database
    context = {
        "pizza_order": Cart.objects.get(username__username=request.session["user"]).order_pizza,
        "pizza_order_topping": Cart.objects.get(username__username=request.session["user"]).order_pizza_topping,
        "pasta_order": Cart.objects.get(username__username=request.session["user"]).order_pasta,
        "salad_order": Cart.objects.get(username__username=request.session["user"]).order_salad,
        "dinner_platter_order": Cart.objects.get(username__username=request.session["user"]).order_dinner_platter,
        "sub_order": Cart.objects.get(username__username=request.session["user"]).order_sub,
        "extra": Cart.objects.get(username__username=request.session["user"]).order_extra,
        "selections": Cart.objects.get(username__username=request.session["user"]).order_selections,
        "total": Cart.objects.get(username__username=request.session["user"]).total_price
    }

    return render(request, "menu/storedcart.html", context)
