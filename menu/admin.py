from django.contrib import admin
from .models import Topping, PizzaType, Size, NumOfTopping, Meal, Salad, Pasta, AddExtra, \
    NumExtraOption, SubType, DinnerPlatter, PizzaOrder, Cart, Order, Sub, SubExtraOption
# Register your models here.

admin.site.register(PizzaType)
admin.site.register(Size)
admin.site.register(NumOfTopping)
admin.site.register(Meal)
admin.site.register(Salad)
admin.site.register(Pasta)
admin.site.register(Topping)
admin.site.register(AddExtra)
admin.site.register(NumExtraOption)
admin.site.register(SubType)
admin.site.register(DinnerPlatter)
admin.site.register(PizzaOrder)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Sub)
admin.site.register(SubExtraOption)