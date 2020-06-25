import os
# noinspection PyUnresolvedReferences
from menu.models import Order
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import stripe

stripe.api_key = os.environ.get("SECRET_API_KEY")


def checkout(request):

    total = request.POST["total"]
    pizza_order = request.POST["pizza_order"]
    pasta_order = request.POST["pasta_order"]
    salad_order = request.POST["salad_order"]
    dinner_platter_order = request.POST["dinner_platter_order"]
    context = {
        "total": total,
        "pizza_order": pizza_order,
        "pasta_order": pasta_order,
        "salad_order": salad_order,
        "dinner_platter_order": dinner_platter_order
    }
    return render(request, "checkout/index.html", context)


def charge(request):

    if request.method == "POST":
        print("Date:", request.POST)

        pizza_order = request.POST["pizza_order"]
        pasta_order = request.POST["pasta_order"]
        salad_order = request.POST["salad_order"]
        dinner_platter_order = request.POST["dinner_platter_order"]
        total = float(request.POST["total"]) * 100
        total = int(total)

    customer = stripe.Customer.create(
        name=request.POST["full_name"],
        email=request.POST["email"],
        source=request.POST["stripeToken"]
    )
    charge = stripe.Charge.create(
        customer=customer,
        amount=total,
        currency="usd",
        description="restaurant bill"
    )
    # Store users order for tracking.
    total = total / 100
    entire_order = str(pizza_order) + str(pasta_order) + str(salad_order) + str(dinner_platter_order)
    Order.objects.create(username=User.objects.get(username=request.session["user"]),
                         order=entire_order, total_price=total)

    return redirect(reverse("success", args=[total]))


def success_page(request, args):
    amount = args
    return render(request, "checkout/success.html", {"amount": amount})
