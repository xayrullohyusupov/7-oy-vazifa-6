from django.shortcuts import render, redirect
from Goods import models


def myCart(request):
    cart = models.Cart.objects.get(author=request.user, is_active=True)
    context = {'cart': cart}
    return render(request, 'cart.html', context)


def addProductToCart(request):
    code = request.GET['code']
    quantity = int(request.GET['quantity'])  # convert to int
    product = models.Product.objects.get(generate_code=code)
    cart, _ = models.Cart.objects.get_or_create(author=request.user, is_active=True)
    try:
        cart_product = models.CartProduct.objects.get(cart=cart, product=product)
        cart_product.quantity += quantity
        cart_product.save()
    except models.CartProduct.DoesNotExist:
        models.CartProduct.objects.create(
            product=product, 
            cart=cart,
            quantity=quantity
        )
    return redirect('my_cart')


def substractProductFromCart(request):
    code = request.GET['code']
    quantity = int(request.GET['quantity'])  # convert to int
    product = models.Product.objects.get(generate_code=code)
    cart_product = models.CartProduct.objects.get(cart__author=request.user, cart__is_active=True, product=product)
    cart_product.quantity -= quantity
    if cart_product.quantity <= 0:
        cart_product.delete()
    else:
        cart_product.save()
    return redirect('my_cart')


def deleteProductCart(request):
    code = request.GET['code']
    product = models.Product.objects.get(generate_code=code)
    cart_product = models.CartProduct.objects.get(cart__author=request.user, cart__is_active=True, product=product)
    cart_product.delete()
    return redirect('my_cart')


def CreateOrder(request):
    cart = models.Cart.objects.get(generate_code=request.GET['generate_code'], author=request.user)
    cart_products = models.CartProduct.objects.filter(cart=cart)

    done_products = []

    for cart_product in cart_products:
        if cart_product.quantity <= cart_product.product.quantity:
            cart_product.product.quantity -= cart_product.quantity
            cart_product.product.save()
            done_products.append(cart_product)
        else:
            for product in done_products:
                product.product.quantity += product.quantity
                product.product.save()
            raise ValueError('Qoldiqda kamchilik')

    models.Order.objects.create(
        cart=cart,
        full_name=f"{request.user.first_name}, {request.user.last_name}",
        email=request.user.email,
        phone=request.GET['phone'],
        address=request.GET['address'],
        status=1
    )
    cart.is_active = False
    cart.save()
    
    return redirect('my_cart')
