from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class PizzaType(models.Model):
    pizzatype = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.pizzatype}"


class Size(models.Model):
    size = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.size}"


class NumOfTopping(models.Model):
    num_of_topping = models.IntegerField()

    def __str__(self):
        return f"{self.num_of_topping}"


class Topping(models.Model):
    topping = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.topping}"


class Meal(models.Model):
    meal_type = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.meal_type}"


class Salad(models.Model):
    salad_meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="salad_meal", default=1)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.salad_meal} - ${self.price}"


class Pasta(models.Model):
    type = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.type} - ${self.price}"


class AddExtra(models.Model):
    extra = models.CharField(max_length=40)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Extra {self.extra} - ${self.price}"


class NumExtraOption(models.Model):
    num_extra_option = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.num_extra_option} Extra options,for ${self.price}"


class SubType(models.Model):
    sub_type = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.sub_type}"


class DinnerPlatter(models.Model):
    dinner_meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name="dinner_meal_id", default=1)
    dinner_platter_size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="dinner_platter_size")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.dinner_meal} - ${self.price}"


class PizzaOrder(models.Model):
    pizza_order_type = models.ForeignKey(PizzaType, on_delete=models.CASCADE, related_name="pizza_order_type")
    pizza_order_size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="pizza_order_size")
    pizza_num_of_topping = models.ForeignKey(NumOfTopping, on_delete=models.CASCADE,
                                             related_name="pizza_num_of_topping",
                                             default=1)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.pizza_order_size}, {self.pizza_order_type} Pizza - ${self.price}"


class Cart(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    order_pizza = models.CharField(max_length=100)
    order_pizza_topping = models.CharField(max_length=30)
    order_pasta = models.CharField(max_length=30)
    order_salad = models.CharField(max_length=30)
    order_entire = models.CharField(max_length=200)
    order_dinner_platter = models.CharField(max_length=30)
    order_sub = models.CharField(max_length=30)
    order_extra = models.CharField(max_length=20)
    order_selections = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"User: {self.username} added to their cart:{self.order_entire}. Totalling ${self.total_price}, on {self.date}"


class Order(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"User: '{self.username}' Ordered:{self.order}. Total: ${self.total_price}.Date: {self.date}"


class SubExtraOption(models.Model):
    sub_extra_option = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.sub_extra_option}"


class Sub(models.Model):
    sub_type = models.ForeignKey(SubType, on_delete=models.CASCADE, related_name="sub_type_id", default=1)
    add_extra = models.ForeignKey(AddExtra, on_delete=models.CASCADE, related_name="add_extra", default=1, blank=True,
                                  null=True)
    options_included = models.BooleanField(default=False, null=True)
    num_of_option = models.ForeignKey(NumExtraOption, on_delete=models.CASCADE, blank=True, null=True)
    option = models.ManyToManyField(SubExtraOption)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name="sub_size", default=1)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.sub_type} Sub, {self.size} size - ${self.price}"
